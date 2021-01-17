# Check if image is from official Docker registry
def registry_check(item, container):
    registry = "docker.io"
    if (registry in container.image) or ("/" not in container.image):
        print(
            "%s\t%s\t%s" %
            (item.metadata.namespace,
             item.metadata.name,
             container.image))
