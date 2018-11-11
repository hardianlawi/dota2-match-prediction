import numpy as np
import pandas as pd

from src.utils.features import feature_names


def load_data():

    df = pd.read_csv('../data/matches_data.csv')
    radiants = pd.read_csv('../data/radiant_features.csv')
    dires = pd.read_csv('../data/dire_features.csv')

    assert np.all(radiants.columns ==
                  dires.columns), 'Radiants have different features than dires'
    assert df.shape[0] == radiants.shape[0], 'Number of matches in radiants are different to original matches data'
    assert df.shape[0] == dires.shape[0], 'Number of matches in dires are different to original matches data'
    assert len(feature_names) + 1 == radiants.shape[1]
    assert len(feature_names) + 1 == dires.shape[1]
    assert (radiants['match_id'] == dires['match_id']).all()
    assert (radiants['match_id'] == df['match_id']).all()

    radiants = radiants.\
        rename({col: 'radiant_' + col for col in feature_names}, axis=1).\
        drop('match_id', axis=1)
    dires = dires.\
        rename({col: 'dire_' + col for col in feature_names}, axis=1).\
        drop('match_id', axis=1)
    df = pd.concat([df[['match_id', 'radiant_win']], radiants, dires], axis=1)
    return radiants, dires, df
