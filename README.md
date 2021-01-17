# kubernetes-cmd-line-tool
Command Line Tool that interfaces with a Kubernetes Cluster API and retrieves information on Deployments

## Prereqs
Python 3.x

Follow instructions at https://kind.sigs.k8s.io/docs/user/quick-start/ to quickly create your own cluster locally if you don't already have one.

Please install the Kubernetes Python Client from here: https://github.com/kubernetes-client/python/
Also install the Pick library by "pip install pick"
Install the Argparse library by "pip install argparse"

The base code of this repo originates from the example inside the Kubernetes Python repo at: https://github.com/kubernetes-client/python/blob/master/examples/pod_config_list.py

## Running this tool
Run this tool through the command line by "python kube.py"
Can specify a namespace by "python kube.py --namespace default" for example to search the default namespace
Can specify label selectors to filter by with "python kube.py --selector key1=value1" for example
Can patch deployments to use a mirrored image with "python kube.py -p"
Can list cronjobs with "python kube.py -c"
Can list statefulsets with "python kube.py -s"
Can list daemonsets with "python kube.py -d"
Please note that this script will not run through an IDE, so make sure to run it through the command line

"python kube.py -h" to see usage

## Tests
A basic python linter has been added to a GitHub Actions workflow and can be seen in the .github folder

## Bugs
When patching to the mirrored repos, these deployments fail as the mirrored repo seems to be in a GCP project that doesn't exist any more. Output from docker pull below:

C:\Users\vinit\kubernetes-cmd-line-tool>docker pull eu.gcr.io/oc-docker-mirror/nginx
Using default tag: latest
Error response from daemon: Get https://eu.gcr.io/v2/oc-docker-mirror/nginx/manifests/latest: unknown: Project 'project:oc-docker-mirror' not found or deleted.
