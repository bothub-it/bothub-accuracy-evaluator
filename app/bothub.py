import requests

from app.settings import BOTHUB_APP_URL, BOTHUB_USER_TOKEN, BOTHUB_NLP_URL

headers = {'Authorization': BOTHUB_USER_TOKEN}


def save_on_bothub(args, text, intent):
    data = {'repository': args.repository, 'text': text, 'entities': [], 'intent': intent}
    requests.post('{0}/api/example/new/'.format(BOTHUB_APP_URL), headers=headers, data=data)


def analyze(text, language, token):
    data = {'text': text, 'language': language}
    headers = {'Authorization': token}
    response = requests.post('{}/parse/'.format(BOTHUB_NLP_URL), headers=headers, json=data)
    return response.json()


def get_intent_data(result):
    return result['answer']['intent']


def get_intent_name(result):
    return get_intent_data(result)['name']
