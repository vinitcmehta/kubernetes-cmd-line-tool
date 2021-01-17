from helper import registry_check, print_resource


# List daemonsets from official Docker registry
def list_daemonsets(apps_v1, namespace, labels):
    if namespace is not None:
        ret = apps_v1.list_namespaced_daemon_set(namespace, label_selector=labels)
    else:
        ret = apps_v1.list_daemon_set_for_all_namespaces(watch=False, label_selector=labels)

    print_resource("Daemonset")

    for item in ret.items:
        for container in item.spec.template.spec.containers:
            registry_check(item, container)
