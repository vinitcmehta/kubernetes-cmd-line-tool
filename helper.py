# Check if image is from official Docker registry
def registry_check(item, container):
    registry = "docker.io"
    if (registry in container.image) or ("/" not in container.image):
        print(
            "%s\t%s\t%s" %
            (item.metadata.namespace,
             item.metadata.name,
             container.image))


def print_resource(resource_type):
    print("Listing " + resource_type + "s with images from the official Docker registry:")
    print(
        "%s\t%s\t%s" %
        ("Namespace",
         resource_type + " name",
         "container image"))
