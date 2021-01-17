from helper import registry_check


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
            registry_check(item, container)
