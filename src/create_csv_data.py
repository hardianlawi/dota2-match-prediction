import os
import csv
import click
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

    players = doc['players']
    for i, player in enumerate(players):
        # If there is anyone abandon, don't record match
        if player['abandons']:
            return None
        row['hero_' + str(i)] = player['hero_id']
    row.update({'radiant_win': doc['radiant_win']})
    return row


def to_csv(docs_generator, collection_name, outputs_dir):
    create_dir_if_not_exist(outputs_dir)
    filename = '{}/{}.csv'.format(outputs_dir, collection_name)
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        row_counts = 0
        for doc in tqdm(docs_generator):
            row = parse_one_match(doc)
            if row is None:
                continue
            writer.writerow(row)
            row_counts += 1
    print('Written %d rows to %s' % (row_counts, filename))


@click.command()
@click.option('--collection_name', help='Collection to query from')
@click.option('--outputs_dir', default='data')
def main(collection_name, outputs_dir):
    db = MongoDB()
    docs_generator = db.query_all_data(collection_name)
    to_csv(docs_generator, collection_name, outputs_dir)


if __name__ == '__main__':

    # pylint: disable=no-value-for-parameter
    main()
