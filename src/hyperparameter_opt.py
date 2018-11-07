import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from skopt import BayesSearchCV

import xgboost as xgb


radiant_cols = ['hero_' + str(i) for i in range(5)]
dire_cols = ['hero_' + str(i) for i in range(5, 10)]

filter_cols = ['base_mr']

cont_variables = [
    'agi_gain',
    'attack_range',
    'attack_rate',
    'base_agi',
    'base_armor',
    'base_attack_max',
    'base_attack_min',
    'base_health_regen',
    'base_int',
    'base_mr',
    'base_str',
    'int_gain',
    'legs',
    'move_speed',
    'pro_ban',
    'pro_pick',
    'pro_win',
    'projectile_speed',
    'str_gain',
    'turn_rate',
]

unique_roles = [
    'Carry',
    'Disabler',
    'Durable',
    'Escape',
    'Initiator',
    'Jungler',
    'Nuker',
    'Pusher',
    'Support'
]

unique_primary_attrs = [
    'agi',
    'int',
    'str'
]

feature_names = cont_variables + \
    ['min_' + col for col in cont_variables if col not in filter_cols] + \
    ['max_' + col for col in cont_variables if col not in filter_cols] + [
        'no_agi',
        'no_int',
        'no_str',
        'no_melees',
        'no_Carry',
        'no_Disabler',
        'no_Durable',
        'no_Escape',
        'no_Initiator',
        'no_Jungler',
        'no_Nuker',
        'no_Pusher',
        'no_Support',
    ]


def load_data():

    df = pd.read_csv('./data/matches_data.csv')
    radiants = pd.read_csv('./data/radiant_features.csv')
    dires = pd.read_csv('./data/dire_features.csv')

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


radiants, dires, df = load_data()


estimator = xgb.XGBClassifier(random_state=0, n_jobs=16)

search_spaces = {
    'learning_rate': (0.01, 1.0, 'log-uniform'),
    'min_child_weight': (0, 10),
    'max_depth': (0, 50),
    'max_delta_step': (0, 20),
    'subsample': (0.01, 1.0, 'uniform'),
    'colsample_bytree': (0.01, 1.0, 'uniform'),
    'colsample_bylevel': (0.01, 1.0, 'uniform'),
    'reg_lambda': (1e-9, 1000, 'log-uniform'),
    'reg_alpha': (1e-9, 1.0, 'log-uniform'),
    'gamma': (1e-9, 0.5, 'log-uniform'),
    'n_estimators': (250, 300, 350, 400),
    'scale_pos_weight': (1e-6, 500, 'log-uniform')
}

kf = KFold(5, random_state=0, shuffle=True)

# Classifier
bayes_cv_tuner = BayesSearchCV(
    estimator=estimator,
    search_spaces=search_spaces,
    scoring='accuracy',
    cv=kf,
    n_jobs=2,
    n_points=2,
    n_iter=200,
    verbose=0,
    refit=True,
    random_state=42
)


def status_print(optim_result):
    """Status callback during bayesian hyperparameter search"""

    # Get all the models tested so far in DataFrame format
    all_models = pd.DataFrame(bayes_cv_tuner.cv_results_)

    print('Model #{}\nBest Accuracy: {}\nBest params: {}\n'.format(
        len(all_models),
        np.round(bayes_cv_tuner.best_score_, 4),
        ', '.join([key + '=' + str(value) for key, value in
                   bayes_cv_tuner.best_params_.items()])
    ))


result = bayes_cv_tuner.fit(np.concatenate([radiants.values, dires.values], axis=1),
                            df.match_id.values, callback=status_print)
