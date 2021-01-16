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


def patch(apps_v1, audited_images):
    for audited_image in audited_images:
        deployment = apps_v1.read_namespaced_deployment(audited_image.get("name"), audited_image.get("namespace"))
        if "/" not in audited_image.get("image"):
            new_image = "eu.gcr.io/oc-docker-mirror/" + audited_image.get("image")
        else:
            split_image = audited_image.get("image").split("/")
            new_image = "eu.gcr.io/oc-docker-mirror/" + split_image[1]
        deployment.spec.template.spec.containers[audited_image.get("position")].image = new_image
        api_response = apps_v1.patch_namespaced_deployment(name=audited_image.get("name"),
                                                           namespace=audited_image.get("namespace"),
                                                           body=deployment)
        print("Deployment updated. status='%s'" % str(api_response.status))


def list_cronjobs(batch_v1beta1, namespace, labels):
    if namespace is not None:
        if labels is not None:
            ret = batch_v1beta1.list_namespaced_cron_job(namespace, label_selector=labels)
        else:
            ret = batch_v1beta1.list_namespaced_cron_job(namespace)
    else:
        if labels is not None:
            ret = batch_v1beta1.list_cron_job_for_all_namespaces(watch=False, label_selector=labels)
        else:
            ret = batch_v1beta1.list_cron_job_for_all_namespaces(watch=False)

    print("Listing cronjobs with images from the official Docker registry:")
    print(
        "%s\t%s\t%s" %
        ("Namespace",
         "Cronjob name",
         "container image"))

    for item in ret.items:
        for container in item.spec.jobTemplate.spec.template.spec.containers:
            registry = "docker.io"
            if (registry in container.image) or ("/" not in container.image):
                print(
                    "%s\t%s\t%s" %
                    (item.metadata.namespace,
                     item.metadata.name,
                     container.image))


def list_statefulsets(apps_v1, namespace, labels):
    if namespace is not None:
        if labels is not None:
            ret = apps_v1.list_namespaced_stateful_set(namespace, label_selector=labels)
        else:
            ret = apps_v1.list_namespaced_stateful_set(namespace)
    else:
        if labels is not None:
            ret = apps_v1.list_stateful_set_for_all_namespaces(watch=False, label_selector=labels)
        else:
            ret = apps_v1.list_stateful_set_for_all_namespaces(watch=False)

    print("Listing statefulsets with images from the official Docker registry:")
    print(
        "%s\t%s\t%s" %
        ("Namespace",
         "Statefulset name",
         "container image"))

    for item in ret.items:
        for container in item.spec.template.spec.containers:
            registry = "docker.io"
            if (registry in container.image) or ("/" not in container.image):
                print(
                    "%s\t%s\t%s" %
                    (item.metadata.namespace,
                     item.metadata.name,
                     container.image))


def list_daemonsets(apps_v1, namespace, labels):
    if namespace is not None:
        if labels is not None:
            ret = apps_v1.list_namespaced_daemon_set(namespace, label_selector=labels)
        else:
            ret = apps_v1.list_namespaced_daemon_set(namespace)
    else:
        if labels is not None:
            ret = apps_v1.list_daemon_set_for_all_namespaces(watch=False, label_selector=labels)
        else:
            ret = apps_v1.list_daemon_set_for_all_namespaces(watch=False)

    print("Listing daemonsets with images from the official Docker registry:")
    print(
        "%s\t%s\t%s" %
        ("Namespace",
         "Daemonset name",
         "container image"))

    for item in ret.items:
        for container in item.spec.template.spec.containers:
            registry = "docker.io"
            if (registry in container.image) or ("/" not in container.image):
                print(
                    "%s\t%s\t%s" %
                    (item.metadata.namespace,
                     item.metadata.name,
                     container.image))


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(
        description='List the deployments in the cluster with images from the offical Docker registry')

    # Add the arguments
    my_parser.add_argument('-n', '--namespace',
                           metavar="namespace",
                           type=str,
                           help='the namespace to list from',
                           dest="namespace")

    my_parser.add_argument('-l', '--selector',
                           metavar="selector",
                           type=str,
                           help='the labels to filter the deployment on',
                           dest="labels")

    my_parser.add_argument('-p', '--patch',
                           action='store_true',
                           help='use this flag to patch deployments',
                           dest="patch")

    my_parser.add_argument('-c', '--cronjobs',
                           action='store_true',
                           help='use this flag to list cronjobs',
                           dest="cronjobs")

    my_parser.add_argument('-s', '--statefulsets',
                           action='store_true',
                           help='use this flag to list statefulsets',
                           dest="statefulsets")

    my_parser.add_argument('-d', '--daemonsets',
                           action='store_true',
                           help='use this flag to list daemonsets',
                           dest="daemonsets")

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
    batch_v1beta1 = client.BatchV1beta1Api()

    namespace = args.namespace
    labels = args.labels
    is_patch = args.patch
    is_cronjobs = args.cronjobs
    is_statefulsets = args.statefulsets
    is_daemonsets = args.daemonsets
    if namespace is not None:
        print("The namespace selected is :", namespace)
        if labels is not None:
            ret = apps_v1.list_namespaced_deployment(namespace, label_selector=labels)
        else:
            ret = apps_v1.list_namespaced_deployment(namespace)
    else:
        if labels is not None:
            ret = apps_v1.list_deployment_for_all_namespaces(watch=False, label_selector=labels)
        else:
            ret = apps_v1.list_deployment_for_all_namespaces(watch=False)



    print("Listing deployments with images from the official Docker registry:")
    print(
        "%s\t%s\t%s" %
        ("Namespace",
         "Deployment name",
         "container image"))

    audited_images =[]
    for item in ret.items:
        container_position = 0
        for container in item.spec.template.spec.containers:
            registry = "docker.io"
            if (registry in container.image) or ("/" not in container.image):
                container_dict = {'name': item.metadata.name, 'namespace': item.metadata.namespace,
                        'image': container.image, 'position': container_position}
                audited_images.append(container_dict)
                print(
                    "%s\t%s\t%s" %
                    (item.metadata.namespace,
                    item.metadata.name,
                    container.image))
            container_position += 1

    if is_patch:
        if audited_images == []:
            print("No deployments available to patch")
        else:
            print("Patching deployments")
            patch(apps_v1, audited_images)

    if is_cronjobs:
        list_cronjobs(batch_v1beta1, namespace, labels)

    if is_statefulsets:
        list_statefulsets(apps_v1, namespace, labels)

    if is_daemonsets:
        list_daemonsets(apps_v1, namespace, labels)


if __name__ == '__main__':
    main()
