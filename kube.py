# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Allows you to pick a context and then lists all pods in the chosen context. A
context includes a cluster, a user, and a namespace.

Please install the pick library before running this example.
"""

from kubernetes import client, config
from kubernetes.client import configuration
from pick import pick  # install pick using `pip install pick`
import argparse


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(
        description='List the deployments in the cluster with images from the offical Docker registry')

    # Add the arguments
    my_parser.add_argument('-n', '--namespace',
                           metavar="namespace",
                           type=str,
                           help='the namepsace to list from',
                           dest="namespace")

    # Execute the parse_args() method
    args = my_parser.parse_args()



    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return
    contexts = [context['name'] for context in contexts]
    active_index = contexts.index(active_context['name'])
    option, _ = pick(contexts, title="Pick the context to load",
                     default_index=active_index)
    # Configs can be set in Configuration class directly or using helper
    # utility
    config.load_kube_config(context=option)

    print("Active host is %s" % configuration.Configuration().host)

    apps_v1 = client.AppsV1Api()
    print("Listing deployments with images from the official Docker registry:")
    print(
        "%s\t%s\t%s" %
        ("Namespace",
         "Deployment name",
         "container image"))

    namespace = args.namespace
    if namespace is not None:
        print("The namespace selected is :", namespace)
        ret = apps_v1.list_namespaced_deployment(namespace)
    else:
        ret = apps_v1.list_deployment_for_all_namespaces(watch=False)

    for item in ret.items:
        for container in item.spec.template.spec.containers:
            registry = "docker.io"
            if (registry in container.image) or ("/" not in container.image):
                print(
                    "%s\t%s\t%s" %
                    (item.metadata.namespace,
                    item.metadata.name,
                    container.image))


if __name__ == '__main__':
    main()
