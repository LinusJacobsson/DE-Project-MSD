import matplotlib.pyplot as plt
from scipy.stats import kurtosis
from scipy.stats import skew
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import VarianceThreshold, SelectKBest, f_classif
from numpy import array
from numpy import argmax
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

import pandas as pd
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.sql import functions as F
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.classification import NaiveBayes

from pyspark.sql import SparkSession 
 
spark_session = SparkSession.builder\
        .master("spark://host-192-168-2-139:7077") \
        .appName("Scaling test")\
        .config("spark.dynamicAllocation.enabled", True)\
        .config("spark.dynamicAllocation.shuffleTracking.enabled",True)\
        .config("spark.shuffle.service.enabled", False)\
        .config("spark.dynamicAllocation.executorIdleTimeout","30s")\
        .config("spark.cores.max", 8)\
        .config("spark.ui.reverseProxy", True)\
        .config("spark.ui.reverseProxyUrl", "http://130.238.28.204:4040/")\
        .getOrCreate()



#csv_file = spark_session.read.csv('file:///home/ubuntu/musicdata/')
import time
time_collection = []
for parts in range(1,3):
    section_times = []
    print("Running timing for " + str(parts) + "partitions")
    section_times.append(parts)
    start_time = time.time()
    s_time = time.time()
    
    """ PRE-PROCESSING """
    csv_file = spark_session.read.csv('file:///home/ubuntu/musicdata/').rdd

    csv_file = csv_file.repartition(parts)

    csv_file = csv_file.map(lambda x : [float(c) for c in x[1:-1]]).cache().toDF()

    labels_file = pd.read_table('file:///home/ubuntu/ML/labels.txt')
    labels = labels_file.columns[0]
    labels_list = labels.split(',')
    labels_list = labels_list[1:-1]
    csv_file = csv_file.toDF(*labels_list)
    ignore = ['generaid', "don`t", "i`m", "can`t"]
    assembler = VectorAssembler(
        inputCols=[x for x in csv_file.columns if x not in ignore],
        outputCol='features')

    data_assembled = assembler.transform(csv_file)
    training, test = data_assembled.randomSplit([0.8, 0.2])
    
    section_times.append(time.time()-s_time)
    s_time = time.time()
    
    """ LOGISTIC REGRESSION """
    lr = LogisticRegression(maxIter=10, regParam=0.01, labelCol="generaid")
    # print("LogisticRegression parameters:\n" + lr.explainParams() + "\n")
    model1 = lr.fit(training)
    lr_pred = model1.transform(test)
    lr_evaluator = MulticlassClassificationEvaluator(
        labelCol="generaid", predictionCol="prediction", metricName="accuracy")
    lr_accuracy = lr_evaluator.evaluate(lr_pred)
    print(lr_accuracy)
    
    section_times.append(time.time()-s_time)
    s_time = time.time()

    """ DECISION TREE """
    tree2 = DecisionTreeClassifier(labelCol="generaid")
    tree_model2 = tree2.fit(training)
    tree_predictions = tree_model2.transform(test)
    evaluator = MulticlassClassificationEvaluator(
        labelCol="generaid", predictionCol="prediction", metricName="accuracy")
    tree_accuracy = evaluator.evaluate(tree_predictions)
    print(tree_accuracy)
    
    section_times.append(time.time() - s_time)
    s_time = time.time()

    """ NAIVE BAYES """
    nb = NaiveBayes(smoothing=1.0, modelType="multinomial")
    bayes_model = nb.fit(training)
    bayes_predictions = bayes_model.transform(test)
    bayes_evaluator = MulticlassClassificationEvaluator(labelCol="generaid", predictionCol="prediction",
                                                  metricName="accuracy")
    bayes_accuracy = bayes_evaluator.evaluate(bayes_predictions)
    print(bayes_accuracy)
    
    section_times.append(time.time()-s_time)
    s_time = time.time() - start_time
    section_times.append(s_time)
    time_collection.append(section_times)
    print(section_times)


with open('scaling_results.txt', 'w') as f:
    for timing in time_collection:
        f.write(f"{time}\n")

spark_session.stop()
