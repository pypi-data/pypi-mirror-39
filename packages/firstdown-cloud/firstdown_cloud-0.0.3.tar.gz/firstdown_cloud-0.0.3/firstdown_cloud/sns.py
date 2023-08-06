import boto3


def get_client():
    sns = boto3.client('sns')
    print sns._endpoint.host
    return sns


def create_topic(topic_name):
    sns = get_client()
    return sns.create_topic(Name=topic_name)


def publish_message(topic_arn, message):
    sns = get_client()
    sns.publish(TopicArn=topic_arn, Message=message)


def make_apns_payload(alert, sound, badge, category, thread_id):
    aps = {}
    if alert is not None:
        aps["alert"] = alert
    if sound is not None:
        aps["sound"] = sound
    if badge is not None:
        aps["badge"] = badge
    if category is not None:
        aps["category"] = category
    if thread_id is not None:
        aps["thread-id"] = thread_id
    return aps


def make_gcm_payload(title, message, topic):
    notification = {}
    data = {}
    if message is not None:
        notification["body"] = message
        data["message"] = message
    if title is not None:
        notification["title"] = title
        data["title"] = title
    if topic is not None:
        data["topic"] = topic

    return {"notification": notification, "data": data}


def make_apns_silent_payload():
    return {"content-available": 1}


def make_gcm_silent_payload():
    return {"data": {}}
