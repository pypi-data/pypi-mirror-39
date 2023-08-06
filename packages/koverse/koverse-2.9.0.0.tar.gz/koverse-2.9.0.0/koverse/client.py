#!/usr/bin/python

#__all__ = ['query', 'autoSuggest', 'getSamples']

import sys
import json
import time
import pprint
import base64

from thrift.Thrift import TType, TMessageType, TException, TApplicationException
from thrift.Thrift import TProcessor
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol, TProtocol
try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None

from koverse.thriftgen.ttypes import *
from koverse.thriftgen.queryservice import QueryService
from koverse.thriftgen.usergroup import UserGroupService
from koverse.thriftgen.collection import CollectionService
from koverse.thriftgen.dataflow import DataFlowService
from koverse.thriftgen.resource import ResourceService
from koverse.thriftgen.internal import InternalService
from koverse.thriftgen.security.ttypes import *
from koverse.thriftgen.dataflow.ttypes import *
from koverse.thriftgen.collection.ttypes import *

# TODO: read from a properties / yaml file

USERGROUP_PORT = 12321
QUERY_PORT = 12324
COLLECTION_PORT = 12322
DATAFLOW_PORT = 12320
RESOURCE_PORT = 12327
INTERNAL_PORT = 12331


TVAL_STRING = 1
TVAL_LONG= 2
TVAL_DOUBLE = 3
TVAL_DATE = 4
TVAL_URL = 5
TVAL_IPADDRESS = 6
TVAL_GEO = 7
TVAL_LIST = 8
TVAL_MAP = 9
TVAL_BYTES = 10
TVAL_BOOLEAN = 11

CLIENT_ID = 'defaultClient'
CLIENT_PASSWORD = 'changeMe'

queryClient = None
ugClient = None
collClient = None
dfClient = None
resClient = None
internalClient = None
auth = None

def _getCollClient():
    global collClient
    if collClient is None:
        raise Exception('call connect() first')
    return collClient

def _getUgClient():
    global ugClient
    if ugClient is None:
        raise Exception('call connect() first')
    return ugClient

def _getQueryClient():
    global queryClient
    if queryClient is None:
        raise Exception('call connect() first')
    return queryClient

def _getDfClient():
    global dfClient
    if dfClient is None:
        raise Exception('call connect() first')
    return dfClient

def _getResClient():
    global resClient
    if resClient is None:
        raise Exception('call connect() first')
    return resClient

def _getInternalClient():
    global internalClient
    if internalClient is None:
        raise Exception('call connect() first')
    return internalClient

def setClientCredentials(clientId, password):
    global CLIENT_ID
    global CLIENT_PASSWORD

    CLIENT_ID = clientId
    CLIENT_PASSWORD = password


def authenticate(token):
    """Authenticate with an API token."""

    global auth
    auth = TAuthInfo()
    auth.clientId = CLIENT_ID
    auth.clientPassword = CLIENT_PASSWORD
    auth.apiTokenId = token

    return _getUgClient().authenticateAPIToken(token)


def authenticateUser(user, password):
    """Authentication with a username and password."""
        
    decoded = base64.b64decode(password)
    global auth
    auth = TAuthInfo()
    auth.clientId = CLIENT_ID
    auth.clientPassword = CLIENT_PASSWORD
    auth.authenticatorId = 'koverseDefault'
    parameters = {
        'emailAddress': user,
        'password': decoded
    }

    tUser = _getUgClient().authenticateUser(auth, None, parameters)
    auth.userId = tUser.id
    auth.externalTokens = []
    auth.externalGroups = []


def connect(host):
    """Provide a hostname. Host needs to have the koverse thrift server listening on 12320, 12321, 12322, 12324, 12327. Returns nothing. Raises exception if connection fails."""

    global queryClient
    global ugClient
    global collClient
    global dfClient
    global resClient
    global internalClient

    transport = TSocket.TSocket(host, QUERY_PORT)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    queryClient = QueryService.Client(protocol)
    transport.open()

    transport = TSocket.TSocket(host, USERGROUP_PORT)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    ugClient = UserGroupService.Client(protocol)
    transport.open()

    transport = TSocket.TSocket(host, COLLECTION_PORT)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    collClient = CollectionService.Client(protocol)
    transport.open()

    transport = TSocket.TSocket(host, DATAFLOW_PORT)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    dfClient = DataFlowService.Client(protocol)
    transport.open()

    transport = TSocket.TSocket(host, RESOURCE_PORT)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    resClient = ResourceService.Client(protocol)
    transport.open()

    transport = TSocket.TSocket(host, INTERNAL_PORT)
    transport = TTransport.TFramedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    internalClient = InternalService.Client(protocol)
    transport.open()

# private method
def _convertValue(tval):
    if tval.type == TVAL_STRING:
        return tval.stringValue
    if tval.type == TVAL_LONG:
        return tval.longValue
    if tval.type == TVAL_DOUBLE:
        return tval.doubleValue
    if tval.type == TVAL_DATE:
        return time.gmtime(tval.longValue)
    if tval.type == TVAL_URL:
        return tval.stringValue
    if tval.type == TVAL_IPADDRESS:
        return tval.stringValue
    if tval.type == TVAL_GEO:
        return tval.geoValue
    if tval.type == TVAL_LIST:
        return tval.listValue
    if tval.type == TVAL_MAP:
        return tval.mapValue
    if tval.type == TVAL_BYTES:
        return tval.bytesValue
    if tval.type == TVAL_BOOLEAN:
        return tval.stringValue == 'true' or tval.stringValue == 'True'

# private method
def _populateFields(allValues, pointer):
    tval = allValues[pointer]
    if tval.type == TVAL_LIST:
        return [_populateFields(allValues, inner) for inner in tval.listValue]
    elif tval.type == TVAL_MAP:
        return dict([(inner[0], _populateFields(allValues, inner[1])) for inner in tval.mapValue.items()])
    else:
        return _convertValue(tval)

# private method
def _toDict(rec):
    return _populateFields(rec.allValues, 0)

def printRecord(rec):
    pprint.pprint(rec)

def query(clauses, datasets=[], offset=0, limit=10000, fields=[], asArrays=False):
    """Provide a dict as the query, a list of collection names, and optional offset, limit, and list of fields to be returned. Returns a list of record dicts."""
        
    # TODO: change to using objectQueryByName
    ids = [_getCollClient().getCollectionByName(auth, c).id for c in datasets]

    q = {
        'query': clauses,
        'collectionIds': ids,
        'limit': limit,
        'offset': offset,
        'fieldsToReturn': fields,
        'returnValuesAsArraysWithType': asArrays
    }

    results = _getQueryClient().objectQuery(auth, json.dumps(q))
    for ds in results:
        ds.records = map(_toDict, ds.records)
    return results

def luceneQuery(queryString, datasets=[], auths=[], numRecords=1000, offset=0, fields=[]):

    # 1:security.TAuthInfo auth,
    # 2:string query,
    # 3:list<common.TCollectionId> dataSets,
    # 4:list<security.TAuthorization> auths,
    # 5:i32 numRecords,
    # 6:i64 recordOffset,
    # 7:list<string> fieldsToReturn,
    # 8:bool removeByteArrayFieldValues,
    # 9:i32 maxStringValueLength

    # TODO: add thrift method for querying via lucene by dataset name
    ids = [_getCollClient().getCollectionByName(auth, c).id for c in datasets]

    results = _getQueryClient().luceneQuery(auth, queryString, ids, auths, numRecords, offset, fields, False, 0)
    for ds in results:
        ds.records = map(_toDict, ds.records)
    return results

def autoSuggest(term, datasets=[]):
    """Provide a term and a list of collection names. Returns a list of suggested search terms."""

    return _getQueryClient().autoSuggestByName(auth, term, datasets)

def getSamples(dataset, maxRecords=1000, removeByteArrays=False, maxStringLength=0):
    """Provide a collection name and optional max records to return (default 1000). Returns a list of record dicts."""

    coll = _getCollClient().getCollectionByName(auth, dataset)

    trecs = _getCollClient().getCollectionSample(auth, coll.id, maxRecords, removeByteArrays, maxStringLength)
    return map(_toDict, trecs)

def listDatasets():
    """Lists all collections visible to this user."""

    return _getCollClient().listCollections(auth)

def getDataset(name):
    """Provide a collection name. Returns a collection object."""

    return _getCollClient().getCollectionByName(auth, name)

def createDataset(name, indexingPolicy=None):

    #struct TCollection {
    #	1:optional common.TCollectionId id
    #	2:optional string name
    #	3:optional string description
    #	4:optional common.TIndexingPolicyId indexingPolicyId
    #	5:optional set<string> tags
    #   6:optional common.TUserId userId
    #	7:common.TTimestamp createdTimestamp
    #	8:common.TTimestamp updatedTimestamp
    #	9:common.TTimestamp recordCountUpdatedTimestamp
    #	10:i64 recordCount
    #	11:i64 sizeInBytes
    #	12:TCollectionState state
    #	13:optional list<common.TCollectionGroupPermissionsId> groupPermissionIds
    #	14:list<common.THadoopJobId> hadoopDeleteJobIds
    #	15:i64 version
    #	16:bool deleted
    #	17:bool disableFieldStats
    #	18:bool disableSampling
    #	19:optional i64 fieldStatsMinimumExecutionPeriod
    #	20:optional i64 samplingMinimumExecutionPeriod
    #	21:optional i64 aggregationMinimumExecutionPeriod
    #	22:string versionedCollectionId
    #   23:optional common.TImportFlowId importFlowId // this will go away in 3.0
    #   24:list<common.TImportFlowId> importFlowIds
    #   25:optional TIndexingPolicy indexingPolicy
    #   26:bool ageOffEnabled
    #   27:i64 ageOffDays
    #   28:i64 ageOffIndexDays
    #   29:optional i64 schemaMinimumExecutionPeriod
    #   30:optional i64 indexMinimumExecutionPeriod
    #}

    coll = TCollection()
    coll.name = name

    if not indexingPolicy is None:
        coll.indexingPolicy = indexingPolicy

    coll.responsibleUserId = auth.userId
    coll.deleted = False
    coll.disableFieldStats = False
    coll.disableSampling = False
    coll.fieldStatsMinimumExecutionPeriod = 3600
    coll.samplingMinimumExecutionPeriod = 3600

    return _getCollClient().createCollection(auth, coll)
    
def deleteDataset(dataset):
    return _getCollClient().deleteCollection(auth, dataset)

def repairDataset(datasetID):
    return _getCollClient().repairCollection(auth, datasetID)

# struct TIndexingPolicy {
#	1:optional TIndexingPolicyFieldMode fieldMode
#	2:optional set<string> fields
#	3:optional list<TFieldTypeIndexTermConfigurationPair> fieldTermConfigurations
#	4:optional list<list<TFieldTypePair>> compositeIndexes
#	5:optional bool createValueOnlyIndices
#   6:common.TIndexingPolicyId id
#   7:common.TCollectionId dataSetId
#   8:optional bool foreignLanguageIndexing
#}

def updateIndexingPolicy(datasetID):
    pass

def listAPITokens():
    return _getUgClient().listAPITokens(auth)

def getAPIToken(name):
    """Create an API token that has the same permissions as the logged in user"""
    return _getUgClient().getAPITokenById(auth, name)
    
def createAPIToken(name):
    return _getUgClient().createAPIToken(auth, name)

#def listSourceTypes():
#    """Returns a list of source types."""
#    return dfClient.listSourceTypeDescriptions(auth)

#def getSourceOptions(sourceType):
#    return dfClient.getSourceTypeDescriptionBySourceTypeId(auth)

class TransformJob(object):

    def __init__(self, j):
        self.j = j

    def getProgress(self):
        job = _getDfClient().getTransformJob(auth, self.j.batchJob.jobAbstract.id)
        return job.batchJob.jobAbstract.progress

class Transform(object):

    def __init__(self, t):
        self.t = t

    def run(self, overrideBlocked=False):
        return TransformJob(_getDfClient().createTransformJob(auth, self.t.transformId))

    #def updateParameters(self, params):
    #    for name,value in params.items():
    #        self.setParameter(name, value)
    #
    #    self.t = dfClient.updateTransform(auth, self.t)

    def remove(self):
        pass

    def getParameters(self):
        return self.t.parameters

    def setParameter(self, name, value):
        self.t.parameters[name] = _configValue(value)

    def getJobs(self):
        pass

def listTransformTypes():
    return _getDfClient().getTransformTypes(auth)

def getTransformType(transformTypeID):
    return _getDfClient().getTransformTypeByTypeId(auth, transformTypeID)


#TRANSFORM_SCHEDULE_AUTOMATIC = "automatic"
#TRANSFORM_SCHEDULE_PERIOD = "periodic"

#TRANSFORM_INPUT_DATA_WINDOW_ALL_DATA = "allData"
#TRANSFORM_INPUT_DATA_WINDOW_LAST_BATCH = "lastBatch"
#TRANSFORM_INPUT_DATA_WINDOW_SLIDING_WINDOW = "slidingWindow"

def showTransformTypeParameters(transformType):
    
    for param in transformType.parameters:
        print('type: {}'.format(param.parameterType))
        print('display name: {}'.format(param.displayName))
        print('hint: {}'.format(param.hint))
        print('\n')

#struct TTransform {
#	1:optional common.TTransformId transformId,
#	2:optional string name,
#	3:optional string type,
#	4:optional common.TUserId userId,
#	5:optional list<common.TJobId> jobIds,
#	6:optional map<string,common.TConfigValue> parameters,
#	7:optional string backend,
#	8:optional bool disabled,
#	9:optional common.TTimestamp creationDate,
#	10:optional common.TTimestamp lastUpdatedDate,
#	11:optional bool replaceOutputData,
#	12:optional string scheduleType,
#	13:optional i64 minimumExecutionPeriod,
#	14:optional string inputDataWindowType,
#	15:optional i64 inputDataSlidingWindowSizeSeconds,
#  16:optional i64 inputDataSlidingWindowOffsetSeconds
#  17:optional TEmailAlertConfiguration emailAlertConfiguration
#}

def createTransform(ttype, inputDatasetIDs, outputDatasetID, options={}, parameters={}):

    t = TTransform()

    t.inputDataWindow = options.get('inputDataWindowTypes', 'allData')
    t.inputDataSlidingWindowSizeSeconds = options.get('inputDataSlidingWindowSizeSecond', 3600)        
    t.scheduleType = options.get('scheduleType', 'automatic')
    t.name = options.get('name', '')

    t.parameters = {
        'outputCollection': TConfigValue(stringValue=outputDatasetID, type=0),
        'inputCollection': TConfigValue(type=3, stringList=inputDatasetIDs)
    }

    for name, value in parameters.items():
        t.parameters[name] = _configValue(value)

    t.replaceOutputData = options.get('replaceOutputData', True)
    t.minimumExecutionPeriod = options.get('minimumExecutionPeriod', 30)
    #t.disabled=False
    #t.lastUpdatedDate=0
    #t.creationDate=0
    t.type = ttype.jobTypeId
    t.inputDataSlidingWindowOffsetSeconds = options.get('inputDataSlidingWindowOffsetSeconds', 0)
    #t.backend='MAP_REDUCE'
    
    return Transform(_getDfClient().createTransform(auth, t))


def _configValue(value):
    if type(value) == str:
        return TConfigValue(stringValue=value, type=TConfigValueType.STRING)

    if type(value) == float:
        return TConfigValue(doubleValue=value, type=TConfigValueType.DOUBLE)

    if type(value) == int:
        return TConfigValue(longValue=value, type=TConfigValueType.LONG)

    if type(value) == list:
        if len(value) == 0 or type(value[0]) == str:
            return TConfigValue(stringList=value, type=TConfigValueType.STRING_LIST)
        if type(value[0]) == float:
            return TConfigValue(doubleList=value, type=TConfigValueType.DOUBLE_LIST)
        if type(value[0]) == int:
            return TConfigValue(longList=value, type=TConfigValueType.LONG_LIST)

    raise TypeError('config value of type: ' + type(value) + ' unsupported')

#def listTransforms(ttype='all'):
#    if ttype == 'all':
#        return map(Transform, dfClient.listTransforms(auth))
#    else:
#        return map(Transform, dfClient.getTransformsByType(auth, ttype))

def listTransforms(datasetID):
    return [Transform(t) for t in _getDfClient().listDataSetTransforms(auth, datasetID)]
    
#def getTransform(name):
#    return Transform(_getDfClient().getTransformByName(auth, name))


#def importData(sourceType, dataset, options):
#    
#    source = {
#        sourceTypeId: sourceType,
#    	name:"" + Math.random(),
#    	configurationOptions:{
#    		options
#        }
#    }
#    
#    dfClient.createSource(auth, source)

def storeResourceFile(filename, data):

    resource = _getResClient().createResource(auth, filename)
    _getResClient().appendDataToResource(auth, resource, data)
    return resource.fileName

# private methods used for spark

def getTransformConfig(transformJobId):
    return _getInternalClient().getTransformJobConfig(auth, transformJobId)

def commitTransformOutput(datasetName, outputPath, transformJobId):
    return _getInternalClient().markPySparkTransformComplete(auth, datasetName, outputPath, transformJobId)

def markTransformFailed(transformJobId, errorMessage):
    return _getInternalClient().markTransformFailure(auth, transformJobId, errorMessage)

def getSparkRddConf(datasetName):
    return _getCollClient().getSparkRDDConf(auth, datasetName)

def getSparkRdd(datasetName, sparkContext):
    conf = _getCollClient().getSparkRDDConf(auth, datasetName)
    return getSparkRddForConf(conf, sparkContext)

def getSparkRddForConf(conf, sparkContext):

    rdd = sparkContext.newAPIHadoopRDD(
        'com.koverse.server.job.transform.KoverseInputFormat',
        'org.apache.hadoop.io.Text',
        'java.util.Map',
        conf = conf)
    return rdd.map(lambda r: r[1])

def getNewSparkJobOutputPath():
    return _getCollClient().getNewSparkJobOutputPath(auth)

def addFilesToDataset(datasetName, outputPath):
    return _getCollClient().addSparkFilesToCollection(auth, datasetName, outputPath)

def cleanupSparkImportDir(importId):
    return _getCollClient().cleanupSparkImportDir(auth, importId)

class Struct:
    def __init__(self, **entries): self.__dict__.update(entries)

def getSparkRdds(rddConfs, sparkContext):
    rdds = {}

    for name,conf in rddConfs.items():
        rdds[name] = getSparkRddForConf(conf, sparkContext)

    return rdds

def getTransformContext(inputRdds, sparkContext, sqlContext=None):

    # setup data frames
    inputDataFrames = {}

    if not sqlContext is None:
        def defGetFieldTypes(rec):
            sortedFields = rec.keys()
            sortedFields.sort()
        for name,rdd in inputRdds.items():
            from pyspark.sql import Row
            rows = rdd.map(lambda rec: replaceNulls(rec))
            df = sqlContext.createDataFrame(rows)
            inputDataFrames[name] = df

    # put into a context object
    # from http://norvig.com/python-iaq.html
    class Struct:
        def __init__(self, **entries): self.__dict__.update(entries)

    context = Struct(inputRdds=inputRdds, inputDataFrames=inputDataFrames, sparkContext=sparkContext, sqlContext=sqlContext)

    return context

def replaceNulls(record, nullReplacement=''):
    for key in record:
        if record[key] is None:
            record[key] = nullReplacement

    from pyspark.sql import Row
    return Row(**record)
