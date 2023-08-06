from pyspark import SparkContext

import sys
sys.path.append('../')
from koverse import client

internalSc = None
internalSQLContext = None

def getSc():
    global internalSc

    if internalSc is None:
        internalSc = SparkContext('local', 'PySparkTransformTestRunner')

    return internalSc

def getSQLContext():
    global internalSQLContext

    if internalSQLContext is None:
        from pyspark.sql import SQLContext
        internalSQLContext = SQLContext(getSc())

    return internalSQLContext

class PySparkTransformTestRunner(object):
    '''This class can be used to test new PySparkTransforms by running them on local or remote data'''

    def __init__(self, params, transformClass):
        self.params = params
        self.transformClass = transformClass

    def testOnLocalData(self, inputDatasets, sc=None, sqlContext=None):

        if sc is None:
            sc = getSc()

        if sqlContext is None:
            sqlContext = getSQLContext()

        # create a set of RDDs for the input records
        rdds = {}
        i = 0
        for inputDataset in inputDatasets:
            rdd = sc.parallelize(inputDataset)
            rdds[str(i)] = rdd
            i += 1

        context = client.getTransformContext(rdds, sc, sqlContext)

        return self._runTest(context)

    def testOnRemoteData(self, remoteDatasets, hostname, username, password, sc=None, sqlContext=None):
        client.connect(hostname)
        client.authenticateUser(username, password)

        if sc is None:
            sc = getSc()

        if sqlContext is None:
            sqlContext = getSQLContext()

        rddConfs = {}
        for remoteDataset in remoteDatasets:
            conf = client.getSparkRDDConf(remoteDataset)
            rddConfs[remoteDataset] = conf

        rdds = client.getSparkRdds(rddConfs, sc)

        context = client.getTransformContext(rdds, sc, sqlContext)

        return self._runTest(context)

    # internal
    def _runTest(self, context):

        transform = self.transformClass(self.params)

        return transform.execute(context)
