import argparse
import json
import os
import traceback

import requests

from app.settings import BOTHUB_USER_TOKEN, BOTHUB_APP_URL


headers = {'Authorization': BOTHUB_USER_TOKEN}

parser = argparse.ArgumentParser(description='Test the accuracy and compare wit.ai and Bothub')

sub_tasks = parser.add_subparsers(title='Tasks')


def fill_bothub(args):
    intent = None
    expressions = None

    files = os.listdir(args.source)

    for filename in files:
        file_item = os.path.join(args.source, filename)

        if os.path.isdir(file_item) and filename == 'entities':
            intent = get_intent(args.intent, file_item)
        elif filename == 'expressions.json':
            expressions = load_json_file(file_item)

    for expression in expressions['data']:
        try:
            entity = expression['entities'][0]
            entity_name = entity['entity']

            if entity_name == args.intent:
                value = entity['value'].strip('\"')
                print('{}: {}'.format(expression['text'], value))

                save_on_bothub(args, expression['text'], value)
        except:
            traceback.print_exc()
            print('Skipping expression {} due to an error'.format(expression))


def save_on_bothub(args, text, intent):
    data = {'repository': args.repository, 'text': text, 'entities': [], 'intent': intent}
    requests.post('{0}/api/example/new/'.format(BOTHUB_APP_URL), headers=headers, data=data)


def get_intent(intent, file_item):
    entities_files = os.listdir(file_item)

    for entity_filename in entities_files:
        entity_file = os.path.join(file_item, entity_filename)
        data = load_json_file(entity_file)

        if intent in data['data']['name']:
            return data
    return None


def load_json_file(entity_file):
    with open(entity_file) as json_file:
        data = json.load(json_file)
    return data


task_fill_bothub = sub_tasks.add_parser('fill_bothub', help='Insert data from a source to Bothub')
task_fill_bothub.add_argument('--source', help='path to the source file, e.g. intents.json')
task_fill_bothub.add_argument('--intent', help='name of the entity that represents the intents')
task_fill_bothub.add_argument('--repository', help='repository uuid destination on bothub')
task_fill_bothub.set_defaults(func=fill_bothub)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
