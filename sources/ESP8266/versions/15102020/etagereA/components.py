components = []


def get_components(file_path="components.txt"):
    # get the list of components stored in the configuration file
    f = open(file_path)
    content = f.read()
    f.close()
    choix = content.split("\n")
    components = []
    for kv in choix:
        if kv != "":
            components.append(kv.strip())
    return components


if len(components) == 0:
    try:
        components = get_components()
    except:
        print("no components")

