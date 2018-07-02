import argparse
import traceback

from app import bothub, wit
from app.bothub import save_on_bothub
from app.utils import percentage
from app.wit import get_expressions_data

parser = argparse.ArgumentParser(description='Test the accuracy and compare wit.ai and Bothub')

sub_tasks = parser.add_subparsers(title='Tasks')


def fill_bothub(args):
    expressions = get_expressions_data(args.source)

    for expression in expressions['data']:
        try:
            entity = expression['entities'][0]
            entity_name = entity['entity']

            if entity_name == args.intent:
                value = entity['value'].strip('\"')
                print('{}: {}'.format(expression['text'], value))

                save_on_bothub(args, expression['text'], value)
        except KeyError:
            traceback.print_exc()
            print('Skipping expression {} due to an error'.format(expression))


task_fill_bothub = sub_tasks.add_parser('fill_bothub', help='Insert data from a source to Bothub')
task_fill_bothub.add_argument('--repository', help='repository uuid destination on bothub')
task_fill_bothub.add_argument('--source', help='path to the source file, e.g. intents.json')
task_fill_bothub.add_argument('--intent', help='name of the entity that represents the intents')
task_fill_bothub.set_defaults(func=fill_bothub)


def predict(args):
    count = 0
    sum_bothub_hits = 0
    sum_bothub_confidence = 0

    sum_wit_hits = 0
    sum_wit_confidence = 0

    expressions = get_expressions_data(args.source)
    for expression in expressions['data']:
        try:
            entity = expression['entities'][0]
            intent_name = entity['entity']

            if intent_name == args.intent:
                count += 1
                value = entity['value'].strip('\"')

                bothub_result = bothub.analyze(value, args.lang, args.authorization_bothub)
                wit_result = wit.analyze(value, args.authorization_wit)

                bothub_intent = bothub.get_intent_data(bothub_result)
                sum_bothub_hits += 1 if bothub_intent['name'] == value else 0
                sum_bothub_confidence += bothub_intent['confidence']

                wit_intent = wit.get_intent_data(wit_result, args.intent)
                sum_wit_hits += 1 if wit_intent['value'] == value else 0
                sum_wit_confidence += wit_intent['confidence']

                print('Processing {}'.format(count))
        except KeyError:
            traceback.print_exc()
            print('Skipping expression {} due to an error'.format(expression))

    print('============================ RESULT ================================')
    bothub_accuracy = percentage(sum_bothub_hits, count)
    bothub_confidence_avg = sum_bothub_confidence/count

    wit_accuracy = percentage(sum_wit_hits, count)
    wit_confidence_avg = sum_wit_confidence/count

    print('Bothub:')
    print('Final Accuracy: {}'.format(bothub_accuracy))
    print('Average Confidence: {}%'.format(bothub_confidence_avg))

    print('Wit:')
    print('Final Accuracy: {}'.format(wit_accuracy))
    print('Average Confidence: {}%'.format(wit_confidence_avg))


task_predict = sub_tasks.add_parser('predict', help='Predict from wit.ai and Bothub and check accuracy')
task_predict.add_argument('--authorization-wit', help='authorization token from dataset on Wit.ai')
task_predict.add_argument('--authorization-bothub', help='authorization token from dataset on Bothub')
task_predict.add_argument('--source', help='path to the source file, e.g. intents.json')
task_predict.add_argument('--intent', help='name of the entity that represents the intents')
task_predict.add_argument('--lang', help='language of the bot on Bothub')
task_predict.set_defaults(func=predict)


if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
