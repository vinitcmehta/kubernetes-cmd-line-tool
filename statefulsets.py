from helper import registry_check, print_resource


# List statefulsets from official Docker registry
def list_statefulsets(apps_v1, namespace, labels):
    if namespace is not None:
        ret = apps_v1.list_namespaced_stateful_set(namespace, label_selector=labels)
    else:
        ret = apps_v1.list_stateful_set_for_all_namespaces(watch=False, label_selector=labels)

    print_resource("Statefulset")

    for item in ret.items:
        for container in item.spec.template.spec.containers:
            registry_check(item, container)
