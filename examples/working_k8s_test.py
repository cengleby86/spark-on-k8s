from pyspark import SparkConf 
from pyspark.sql import SparkSession 
from pyspark.sql import Row
from datetime import datetime, date
import socket
import pandas as pd
import os

host_ip = socket.gethostbyname(socket.gethostname())
print(host_ip)

# Set the configuration for the SparkSession
conf = SparkConf() \
    .setAppName("Event Driven Spark") \
    .setMaster("k8s://https://<kube-api>:6443") \
    .set("spark.kubernetes.container.image", "quay.io/rh_ee_cengleby/apache-spark:3.4.1.1") \
    .set("spark.kubernetes.namespace", "spark-events") \
    .set("spark.executor.instances", "1") \
    .set("spark.executor.memory","2g") \
    .set("spark.driver.memory","512m") \
    .set("spark.driver.host", host_ip) \
    .set("spark.driver.bindAddress", "0.0.0.0") \
    .set("spark.submit.deployMode", "client") \
    .set("spark.kubernetes.driver.scheduler.name", "spark-events-dataframe-job") \
    .set("spark.kubernetes.executor.podTemplateFile","podtemplate.yaml") \
    .set("spark.kubernetes.authenticate.serviceAccountName", "jupyter-notebooks")

spark = SparkSession.builder.config(conf=conf).getOrCreate() 

sc = spark.sparkContext
sc.setLogLevel("ERROR")

print('\nSpark Version: ', sc.version) 
print('Spark Application ID: ', sc.applicationId) 

pandas_df = pd.DataFrame({
    'a': [1, 2, 3],
   
    'b': [4., 8., 5.],
   
    'c': ['GFG1', 'GFG2', 'GFG3'],
   
    'd': [date(2000, 8, 1), date(2000, 6, 2),
          date(2000, 5, 3)],
   
    'e': [datetime(2000, 8, 1, 12, 0),
          datetime(2000, 6, 2, 12, 0),
          datetime(2000, 5, 3, 12, 0)]
})
 
df = spark.createDataFrame(pandas_df)
df.show()

spark.stop()