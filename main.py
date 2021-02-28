from slacker import Slacker
import json
from flask import Flask, request, make_response
token = 'xoxb-1698891588323-1809948168225-v1TU7HrtJ0r6dWeBmSCNt6Fa'
slack = Slacker(token)


app = Flask(__name__)




def get_answer_add(event_name):
    return "새로운 이모티콘이 추가됐카! [ :" + event_name + ": ] (:" + event_name+") 을 써보라카! "

def get_answer_remove(event_name):
    return event_name + "이모지가 삭제되었어요 ㅠㅠ RIP"

def get_answer_rename(old, new):
    return "이모지 이름이 [" +old + "] 에서 [" + new + "] 로 바뀌었습니다!! " + ":" + new + ":"


def event_handler(event_type, event_name, event_subtype, slack_event):

    if event_type == "emoji_changed":
        if event_subtype == "add":
            text = get_answer_add(event_name)
        if event_subtype == "remove":
            text = get_answer_remove(event_name)
        if event_subtype == "rename":
            old = slack_event["event"]["old_name"]
            new = slack_event["event"]["new_name"]
            text = get_answer_rename(old, new)

        slack.chat.post_message("#랜덤", text)
        return make_response("이모지가 만들어졌습니다!", 200,)
    message = "[%s] 이벤트 핸들러를 찾을 수 없습니다. " %event_type
    return make_response(message, 200, {"X-Slack-No_Retry": 1})

@app.route("/slack", methods=["GET","POST"])


def hears():
    slack_event =json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"],200,{"content_type": "application/json"})

    if "event" in slack_event:

        event_type = slack_event["event"]["type"]
        event_name = slack_event["event"]["name"]
        event_subtype = slack_event["event"]["subtype"]

        return event_handler(event_type, event_name, event_subtype, slack_event)

    return make_response("슬랙 요청에 이벤트가 없습니다", 404, {"X-Slack-No_Retry" : 1})


@app.route("/", methods=["GET","POST"])

def index():
    return "Hello World"

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
