# Jupyter Notebooks



oc create secret generic spark-driver-kubeconfig \
    --from-file=config=/path/to/your/kubeconfig -n jupyter-notebooks