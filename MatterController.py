import slackweb
from flask import request
from config import matter_conf as config

def botbot_information(attachment):
    params = config()
    attachments = []
    attachments.append(attachment)
    mattermost = slackweb.Slack(url=params['webhooks'])
    mattermost.notify(text="", attachments=attachments)
