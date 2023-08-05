from pyspark.sql import SparkSession
import tensorflow as tf
from pyspark.ml.feature import VectorAssembler, Normalizer
from sparkflow.tensorflow_async import SparkAsyncDL, SparkAsyncDLModel
from pyspark.sql.functions import rand
from sparkflow.graph_utils import build_graph


def small_model():
    x = tf.placeholder("float", shape=[None, 784], name='x')
    layer1 = tf.layers.dense(x, 256, activation=tf.nn.sigmoid)
    layer2 = tf.layers.dense(layer1, 128, activation=tf.nn.sigmoid)
    layer3 = tf.layers.dense(layer2, 256, activation=tf.nn.sigmoid)
    layer4 = tf.layers.dense(layer3, 784, activation=tf.nn.sigmoid)
    loss = tf.losses.mean_squared_error(layer4, x)
    return loss

if __name__ == '__main__':
    spark = SparkSession.builder \
        .appName("examples") \
        .master('local[8]').config('spark.driver.memory', '4g') \
        .getOrCreate()

    df = spark.read.option("inferSchema", "true").csv('mnist_train.csv').orderBy(rand())
    mg = build_graph(small_model)

    va = VectorAssembler(inputCols=df.columns[1:785], outputCol='feats').transform(df).select(['feats'])
    na = Normalizer(inputCol='feats', outputCol='features', p=1.0).transform(va).select(['features'])

    #demonstration of options. Not all are required
    spark_model = SparkAsyncDL(
        inputCol='features',
        tensorflowGraph=mg,
        tfInput='x:0',
        tfLabel=None,
        tfOutput='out:0',
        tfOptimizer='adam',
        tfLearningRate=.001,
        iters=10,
        predictionCol='predicted',
        partitions=3,
        miniBatchSize=256,
        verbose=1
    ).fit(na)

    spark_model.fit(na).save('auto_encoded')
    x = SparkAsyncDLModel.load("auto_encoded").transform(na).take(10)
    print(x)
