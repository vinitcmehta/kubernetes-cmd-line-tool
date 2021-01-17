from helper import registry_check, print_resource


# List cronjobs from official Docker registry
def list_cronjobs(batch_v1beta1, namespace, labels):
    if namespace is not None:
        ret = batch_v1beta1.list_namespaced_cron_job(namespace, label_selector=labels)
    else:
        ret = batch_v1beta1.list_cron_job_for_all_namespaces(watch=False, label_selector=labels)

    print_resource("Cronjob")

    for item in ret.items:
        for container in item.spec.jobTemplate.spec.template.spec.containers:
            registry_check(item, container)
