import requests

from app.settings import BOTHUB_APP_URL, BOTHUB_USER_TOKEN

headers = {'Authorization': BOTHUB_USER_TOKEN}


def save_on_bothub(args, text, intent):
    data = {'repository': args.repository, 'text': text, 'entities': [], 'intent': intent}
    requests.post('{0}/api/example/new/'.format(BOTHUB_APP_URL), headers=headers, data=data)
