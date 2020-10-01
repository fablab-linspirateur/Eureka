TOPIC_SEARCH_BASE = "search"
TOPIC_END = "end"
TOPIC_ERROR_BASE = "error"


def init_mqtt(client, sleep_ms):
    # initialize mqtt subscriptions

    from components import components
    from leds import init_component_leds, neo_write, to_neopixel, display_component, turn_off, display_error
    init_component_leds(components)

    def refresh(topic, payload):
        # refresh display on topic action
        from topics import explode_topic
        etopic = explode_topic(topic.decode("utf-8"))
        if etopic["base"] == TOPIC_SEARCH_BASE:
            display_component(etopic["info"], int(payload))
        elif etopic["base"] == TOPIC_END:
            turn_off(int(payload))
        elif etopic["base"] == TOPIC_ERROR_BASE:
            display_error(etopic["info"], int(payload))
        neo_write(to_neopixel(components), sleep_ms)

    client.set_callback(refresh)
    client.subscribe(TOPIC_SEARCH_BASE + "/#")
    client.subscribe(TOPIC_END)
    client.subscribe(TOPIC_ERROR_BASE + "/#")

