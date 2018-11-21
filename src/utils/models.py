import tensorflow as tf
from sklearn.preprocessing import StandardScaler

from src.utils.features import feature_names


def define_model(name, optimizer='adam', seed=0,
                 learning_rate=0.001, unit_size=16, activation='relu',
                 dropout_rate=0.2, alpha=0.01):

    if optimizer == 'adam':
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    elif optimizer == 'sgd':
        optimizer = tf.train.GradientDescentOptimizer(
            learning_rate=learning_rate)
    else:
        raise Exception

    x1 = tf.keras.layers.Input(
        shape=[len(feature_names)], name='input_radiant')
    x2 = tf.keras.layers.Input(
        shape=[len(feature_names)], name='input_dire')

    inputs = [x1, x2]

    if name == 'nn_tanh':
        x = tf.keras.layers.Concatenate()([x1, x2])
        x = tf.keras.layers.Dense(unit_size, activation='tanh')(x)
        x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    elif name == 'nn_relu':
        x = tf.keras.layers.Concatenate()([x1, x2])
        x = tf.keras.layers.Dense(unit_size, activation='relu')(x)
        x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    elif name == 'custom_nn':
        dense = tf.keras.layers.Dense(unit_size // 2, activation=activation)
        x = tf.keras.layers.Concatenate()([dense(x1), dense(x2)])
        x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    elif name == 'custom_nn_l2_regularizer':
        dense = tf.keras.layers.Dense(unit_size // 2, activation=activation,
                                      kernel_regularizer=tf.keras.regularizers.l2(alpha))
        x = tf.keras.layers.Concatenate()([dense(x1), dense(x2)])
        x = tf.keras.layers.Dense(1, activation='sigmoid',
                                  kernel_regularizer=tf.keras.regularizers.l2(alpha))(x)
    elif name == 'custom_nn_dropout':
        dense = tf.keras.layers.Dense(unit_size // 2, activation=activation)
        x = tf.keras.layers.Concatenate()([dense(x1), dense(x2)])
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    elif name == 'nn_l2_regularizer':
        x = tf.keras.layers.Concatenate()([x1, x2])
        x = tf.keras.layers.Dense(unit_size, activation=activation,
                                  kernel_regularizer=tf.keras.regularizers.l2(alpha))(x)
        x = tf.keras.layers.Dense(1, activation='sigmoid',
                                  kernel_regularizer=tf.keras.regularizers.l2(alpha))(x)
    elif name == 'nn_dropout':
        x = tf.keras.layers.Concatenate()([x1, x2])
        x = tf.keras.layers.Dropout(0.5, seed=seed)(x)
        x = tf.keras.layers.Dense(unit_size, activation=activation)(x)
        x = tf.keras.layers.Dropout(dropout_rate, seed=seed)(x)
        x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
    else:
        raise Exception

    model = tf.keras.Model(inputs=inputs, outputs=x)
    model.compile(optimizer, loss='binary_crossentropy', metrics=['acc'])

    return model


def train_and_pred(models, X_train, y_train, X_test, y_test, key,
                   batch_size=128, epochs=60):

    y_preds_train = 0
    y_preds_test = 0

    if isinstance(X_train, list) and isinstance(X_test, list):
        radiant_scaler = StandardScaler()
        dire_scaler = StandardScaler()
        X_train = [radiant_scaler.fit_transform(
            X_train[0]), dire_scaler.fit_transform(X_train[1])]
        X_test = [radiant_scaler.transform(
            X_test[0]), dire_scaler.transform(X_test[1])]
    else:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    for j, model in enumerate(models):

        history = model.fit(X_train, y_train,
                            validation_data=(X_test, y_test),
                            batch_size=batch_size,
                            epochs=epochs,
                            verbose=0)

        y_preds_train += model.predict(X_train)
        y_preds_test += model.predict(X_test)

    y_preds_train /= len(models)
    y_preds_test /= len(models)

    return y_preds_train, y_preds_test, history
