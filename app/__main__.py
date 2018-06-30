import argparse
import os
import traceback

from app.bothub import save_on_bothub
from app.utils import load_json_file

parser = argparse.ArgumentParser(description='Test the accuracy and compare wit.ai and Bothub')

sub_tasks = parser.add_subparsers(title='Tasks')


def fill_bothub(args):
    expressions = None

    files = os.listdir(args.source)
    for filename in files:
        file_item = os.path.join(args.source, filename)

        if filename == 'expressions.json':
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


task_fill_bothub = sub_tasks.add_parser('fill_bothub', help='Insert data from a source to Bothub')
task_fill_bothub.add_argument('--source', help='path to the source file, e.g. intents.json')
task_fill_bothub.add_argument('--intent', help='name of the entity that represents the intents')
task_fill_bothub.add_argument('--repository', help='repository uuid destination on bothub')
task_fill_bothub.set_defaults(func=fill_bothub)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
