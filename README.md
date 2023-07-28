## Apache Spark on Kubernetes

Running Apache Spark on Kubernetes has several advantages compared to the traditional standalone cluster or other cluster managers like Hadoop YARN or Mesos:

- **Resource Efficiency**: In Kubernetes, pods are ephemeral and they consume resources only when a job is running. This leads to better resource utilization as compared to standalone mode where resources are statically partitioned.
  
- **Dynamic Scaling**: Kubernetes provides the ability to dynamically scale the number of Spark executors and hence can adjust to the load dynamically.

- **Isolation**: Each Spark application runs in its own namespace which provides isolation from other applications. This is beneficial for multi-tenancy situations, where multiple users or teams are sharing the cluster.

- **Portability**: A Kubernetes-based infrastructure is cloud-agnostic. This means you can move your Spark workloads across different cloud environments or on-premises easily.

- **Integration with advanced Kubernetes features**: Running Spark on Kubernetes allows you to take advantage of advanced Kubernetes features like custom resources, operators, service meshes, and so on.

- **Consistent Environment**: If your other applications (web servers, databases, etc.) are already running on Kubernetes, running Spark on Kubernetes can unify your infrastructure under a single platform.

- **Fault Tolerance**: Kubernetes will restart your Spark application if it fails, providing increased reliability and fault-tolerance compared to standalone deployment.

- **Security**: Kubernetes provides robust security features, including Secrets management and ServiceAccount for role-based access control which can be utilized for Spark applications.


Please note that adopting "Spark on Kubernetes" might require more understanding and expertise in Kubernetes. You should consider these trade-offs and your team's familiarity with Kubernetes when choosing a deployment model.

## Architecture

**Kubernetes** (often abbreviated to K8s) is an open-source platform designed to automate deploying, scaling, and operating application containers. It groups containers that make up an application into logical units for easy management and discovery.

**Apache Spark** is a powerful open-source processing engine for data in the Hadoop data lake. It provides a way to speed up the processing of large amounts of data.

**Spark on Kubernetes** refers to running your Spark application's driver and executors as pods in a Kubernetes cluster, instead of on static machines or other cluster managers like YARN or Mesos.

Now let's break it down:

- **Driver**: This is the process that runs your Spark application's main() function and defines the dataset on your cluster, and applies operations to it. In Kubernetes mode, the driver program runs in a Kubernetes pod.
  
- **Executors**: These are the processes that execute the tasks assigned to them by the driver program. In Kubernetes mode, each executor runs in a separate pod within the Kubernetes cluster. Executors read from and write data to datastores, perform computations on the data and report the results back to the driver program.
  
- **Pods**: In Kubernetes, a pod represents a single instance of a running process in a cluster and can host one or multiple containers. The containers in a pod share the same network namespace, including the IP address and network ports.
  

When a Spark application is submitted to a Kubernetes cluster:

- A Docker image of the Spark application is created. This image contains the Spark and its dependencies. The image is then deployed as a driver pod in the Kubernetes cluster.

- The driver pod creates executor pods, each of which can run a task.

- Each executor pod pulls the Docker image of the Spark application and starts executing the tasks assigned to it.

- The driver program divides the Spark application into a series of tasks that are distributed to executor pods.

- The results from these tasks are delivered back to the driver pod, which can then use these results for further processing or save the data to a datastore.


That's the overall picture. There's much more to it - things like how Spark optimizes tasks, how Kubernetes can scale the number of executor pods based on load, and so on. But at a high level, that's how Spark runs on Kubernetes.  For deeper insights visit the documentation located at [Running Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html)

## Getting Started

First we need to create the Role Based Access Controls

```
oc apply -f spark-events/permissions/cluster-role.yaml
oc apply -f spark-events/permissions/cluster-role-bindings.yaml
```

Then we will need to create an environment that is capable of running our drivers( spark-submit | apache airflow w/ pyspark | pyspark jupyter notebooks )

```
oc apply -f spark-events/environments/notebooks.yaml
```

Then we can create a partition to scope spark-jobs.  You may have many partitions depending on how you want to scope your workloads.

```
oc apply -f spark-events/environments/partitions.yaml
```

After we have an partition environment created for spark pods to run inside; we can create a namespace that can host a driver with the capabilities to use a service account that has permissions to control the cluster.

```
oc create secret generic spark-driver-kubeconfig \
	--from-file=config=/path/to/your/kubeconfig -n jupyter-notebooks
oc apply -f jupyter-notebooks/pyspark/notebook.yaml
```

We mount the kubeconfig into the driver pod inorder to authenticate to the k8s:// api endpoint.

### Using Write to Memory

For speed you may wish to not use locally mounted storage but write to ram instead.  This setting allows you to configure tmpfs to use executors ram.

```
park.kubernetes.local.dirs.tmpfs=true
```