# Getting Started

```
Download spark 3.4.1 from spark.apache.org/downloads.html
Extract the contents
```

Navigate to the directory and creating a base image
```
./bin/docker-image-tool.sh -r apache-spark -t 3.4.1.1 -p kubernetes/dockerfiles/spark/bindings/python/Dockerfile build
```

Specs
- python 3.10.6
- pyspark 3.4.1

Set this image in the pyspark script being run


Which notebook matches this setup
docker pull jupyter/pyspark-notebook:spark-3.4.1

- python 3.11.4
- pyspark 3.4.1


You can shim the notebooks with

wget https://bootstrap.pypa.io/get-pip.py
python3.10 get-pip.py
python3.10 -m pip install pandas==1.5.3

Create a kubeconfig secret to mount into pods

```
oc create secret generic kube-config-spark-drivers --from-file=~/.kube/config --namespace=jupyter-notebooks
```

Run workloads