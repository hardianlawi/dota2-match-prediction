import json
import argparse
import logging
from src.database import MongoDB
from src.data_extractor import DataExtractor


def filter_pro_matches(resp):
    """Filter the responses that do not have team name

    Args:
        resp (list): list of dictionaries which each contains the information of a professional match.

    Returns:
        list: filtered list of dictionaries.
    """

    return [x for x in resp if x['dire_name'] and x['radiant_name']]


def main(api, less_than_match_id, pub_matches_records):

    # Initialize API caller and Database
    data_extractor = DataExtractor()
    db = MongoDB()

    if api == 'pro_matches':

        # Query professional matches #
        ##############################

        # Filter query that is less than `less_than_match_id`
        filter_rule = {'match_id': {'$lt': less_than_match_id}}

        # Keep track of the least `match_id`
        match_id = less_than_match_id
        while db.pro_matches.count_documents(filter=filter_rule) < 100000:
            resp = data_extractor.extract_pro_matches_from_api(match_id)
            resp = filter_pro_matches(resp)
            match_id = min(resp, key=lambda x: x.get('match_id'))['match_id']
            db.pro_matches.insert_many(resp)

    elif api == 'matches_data':

        if pub_matches_records is not None:
            with open(pub_matches_records, 'r') as f:
                pub_matches = json.load(f)
                match_ids = [x['match_id'] for x in pub_matches['rows']]
        else:
            assert db.pro_matches_col_exist
            filter_rule = {'match_id': {'$lt': less_than_match_id}}
            match_ids = [x['match_id']
                         for x in db.pro_matches.find(filter_rule, {'match_id': 1})]

        for match_id in match_ids:
            resp = data_extractor.extract_match_data_from_api(match_id)
            db.matches_data.insert_one(resp)

    else:
        raise NotImplementedError('API choice has not been implemented.')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--api', default='pro_matches',
                        description="API to extract the data")
    parser.add_argument('--less_than_match_id', default=4148592604)
    parser.add_argument('--pub_matches_records',
                        description="file containing the public matches records")

    # Parse arguments
    args = parser.parse_args()

    # Assign arguments to variables
    api = args.api
    less_than_match_id = args.less_than_match_id
    pub_matches_records = args.pub_matches_records

    assert api is not None
    assert less_than_match_id is not None

    if pub_matches_records is not None:
        assert api == 'matches_data', 'Set API to matches data'

    # Run main function
    main(api, less_than_match_id, pub_matches_records)
