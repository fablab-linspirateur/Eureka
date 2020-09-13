def explode_topic(topic):
    # retrieve type + info contained in a topic
    ttopic = topic.split("/", 1)
    if len(ttopic) == 1:
        return {"base": ttopic[0], "info": ""}
    else:
        return {"base": ttopic[0], "info": ttopic[1]}
