import os
import csv
import argparse
from tqdm import tqdm

from src.database import MongoDB


FIELDNAMES = [
    'match_id',
]
FIELDNAMES.extend(['hero_%d' % i for i in range(10)])
FIELDNAMES.append('radiant_win')


def create_dir_if_not_exist(outputs_dir):
    if not os.path.exists(outputs_dir):
        os.mkdir(outputs_dir)


def parse_one_match(doc):
    row = {}
    row['match_id'] = doc['match_id']
    row.update({'hero_' + str(i): player['hero_id'] for
                i, player in enumerate(doc['players'])})
    row.update({'radiant_win': doc['radiant_win']})
    return row


def to_csv(docs_generator, collection_name, outputs_dir):
    create_dir_if_not_exist(outputs_dir)
    with open('{}/{}.csv'.format(outputs_dir, collection_name), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for doc in tqdm(docs_generator):
            row = parse_one_match(doc)
            writer.writerow(row)


def main(collection_name, outputs_dir):
    db = MongoDB()
    docs_generator = db.query_all_data(collection_name)
    to_csv(docs_generator, collection_name, outputs_dir)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('collection_name', help='Collection to query from')
    parser.add_argument('--outputs_dir', default='outputs')

    args = parser.parse_args()
    collection_name = args.collection_name
    outputs_dir = args.outputs_dir

    main(collection_name, outputs_dir)
