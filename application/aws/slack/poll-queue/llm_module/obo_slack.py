import requests
import re

def format_message(message):
    REGEX_REPLACE = (
        (re.compile('^- ', flags=re.M), '• '),
        (re.compile('^  - ', flags=re.M), '  ◦ '),
        (re.compile('^    - ', flags=re.M), '    ⬩ '), # ◆
        (re.compile('^      - ', flags=re.M), '    ◽ '),
        (re.compile('^#+ (.+)$', flags=re.M), r'*\1*'),
        (re.compile('\*\*'), '*'),
    ) 
    for regex, replacement in REGEX_REPLACE:
        message = regex.sub(replacement, message)
    return message

def get_thread_history(slack_key, channel_id, thread_ts):
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {slack_key}'
    }
    params = {
        'channel': channel_id,
        'ts': thread_ts
    }
    res = requests.get(url='https://slack.com/api/conversations.replies', headers=headers, params=params)

    if not res.ok:
        return None
    
    res_json = res.json()
    if not res_json['ok']:
        return None

    message_thread = []
    for message in res_json['messages']:
        if 'bot_id' in message:
            message_parse = {
                "bot": True,
                "text": message['text']
            }
        else:
            message_parse = {
                "bot": False,
                "text": message['text']
            }
        try:
            message_parse['files'] = message['files']
        except:
            pass
        message_thread.append(message_parse)
    return message_thread
    
def delete_slack_message(slack_key, channel_id, message_ts):
    url = "https://slack.com/api/chat.delete"

    data = {
        "channel": channel_id,  # The ID of the channel where the message is posted.
        "ts": message_ts  # The 'ts' value of the message to reply to.
    }

    headers = {
        "Content-type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {slack_key}"
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def reply_in_thread(slack_key, channel_id, thread_ts, text):

    url = "https://slack.com/api/chat.postMessage"
    try:
        message = format_message(message=text)
    except:
        message = text
    data = {
        "channel": channel_id,  # The ID of the channel where the message is posted.
        "text": message,  # The text of the message to post.
        "thread_ts": thread_ts  # The 'ts' value of the message to reply to.
    }

    headers = {
        "Content-type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {slack_key}"
    }

    response = requests.post(url, headers=headers, json=data)
    return response
