def get_config(config_file="config.yaml"):
    # get the configuration dictionary from yaml file
    f = open(config_file)
    content = f.read()
    f.close()
    choix = content.split("\n")
    config = {}
    for kv in choix:
        if kv != '':
            key, val = kv.split(":")
            key = key.strip()
            config[key] = val.strip()
    if "port" in config:
        config["port"] = int(config["port"])
    return config
