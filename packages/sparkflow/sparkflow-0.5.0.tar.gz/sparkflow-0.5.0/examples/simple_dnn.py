from pyspark.sql import SparkSession
import tensorflow as tf
from pyspark.ml.feature import VectorAssembler, OneHotEncoder
from sparkflow.tensorflow_async import SparkAsyncDL, SparkAsyncDLModel
from pyspark.sql.functions import rand
from sparkflow.graph_utils import build_graph
from sparkflow.graph_utils import build_adam_config
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def small_model():
    x = tf.placeholder(tf.float32, shape=[None, 784], name='x')
    y = tf.placeholder(tf.float32, shape=[None, 10], name='y')
    layer1 = tf.layers.dense(x, 256, activation=tf.nn.relu)
    layer2 = tf.layers.dense(layer1, 256, activation=tf.nn.relu)
    out = tf.layers.dense(layer2, 10)
    z = tf.argmax(out, 1, name='out')
    loss = tf.losses.softmax_cross_entropy(y, out)
    return loss


if __name__ == '__main__':
    spark = SparkSession.builder \
        .appName("examples") \
        .master('local[8]').config('spark.driver.memory', '4g') \
        .getOrCreate()

    df = spark.read.option("inferSchema", "true").csv('mnist_train.csv').orderBy(rand())
    mg = build_graph(small_model)
    adam_config = build_adam_config(learning_rate=0.001, beta1=0.9, beta2=0.999)

    va = VectorAssembler(inputCols=df.columns[1:785], outputCol='features').transform(df)
    encoded = OneHotEncoder(inputCol='_c0', outputCol='labels', dropLast=False).transform(va).select(['features', 'labels'])

    #demonstration of options. Not all are required
    spark_model = SparkAsyncDL(
        inputCol='features',
        tensorflowGraph=mg,
        tfInput='x:0',
        tfLabel='y:0',
        tfOutput='out:0',
        tfOptimizer='adam',
        miniBatchSize=300,
        miniStochasticIters=1,
        shufflePerIter=True,
        iters=50,
        predictionCol='predicted',
        labelCol='labels',
        partitions=3,
        verbose=1,
        optimizerOptions=adam_config
    )

    spark_model.fit(encoded).save('simple_dnn')
    predictions = SparkAsyncDLModel.load("simple_dnn").transform(encoded)
    evaluator = MulticlassClassificationEvaluator(
        labelCol="labels", predictionCol="predicted", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    print("Test Error = %g" % (1.0 - accuracy))
