# kubernetes-cmd-line-tool
Command Line Tool that interfaces with a Kubernetes Cluster API and retrieves information on Deployments

Follow instructions at https://kind.sigs.k8s.io/docs/user/quick-start/ to quickly create your own cluster locally if you don't already have one.

Please install the Kubernetes Python Client from here: https://github.com/kubernetes-client/python/
Also install the Pick library by "pip install pick"
Install the Argparse library by "pip install argparse"

The base code of this repo originates from the example inside the Kubernetes Python repo at: https://github.com/kubernetes-client/python/blob/master/examples/pod_config_list.py

Running this tool:
Run this tool through the command line by "python kube.py"
Can specify a namespace by "python kube.py --namespace default" for example to search the default namespace
Can specify label selectors to filter by with "python kube.py --selector key1=value1" for example
Please note that this script will not run through an IDE, so make sure to run it through the command line

"python kube.py -h" to see usage


