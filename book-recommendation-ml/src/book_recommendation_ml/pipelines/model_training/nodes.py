import logging

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import tensorflow.compat.v1 as tf
from sklearn.preprocessing import MinMaxScaler

tf.compat.v1.disable_v2_behavior()


def split_data(data: pd.DataFrame, parameters: dict) -> tuple:
    X = data[parameters["features"]]
    y = data["Book-Rating"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> KNeighborsRegressor:
    regressor = KNeighborsRegressor(n_neighbors=5)
    regressor.fit(X_train, y_train)
    return regressor


def evaluate_model(
    regressor: KNeighborsRegressor, X_test: pd.DataFrame, y_test: pd.Series
):
    y_pred = regressor.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("KNN Regressor has a Mean Squared Error of %.3f on test data.", mse)


def normalise_rating(combined: pd.DataFrame):
    scaler = MinMaxScaler()
    combined["Book-Rating"] = combined["Book-Rating"].values.astype(float)
    rating_scaled = pd.DataFrame(
        scaler.fit_transform(combined["Book-Rating"].values.reshape(-1, 1))
    )
    combined["Book-Rating"] = rating_scaled
    return combined


def create_user_book_matrix(combined: pd.DataFrame):
    combined = combined.drop_duplicates(["User-ID", "Book-Title"])
    user_book_matrix = combined.pivot(
        index="User-ID", columns="Book-Title", values="Book-Rating"
    )
    users_list = user_book_matrix.index.tolist()
    books_list = user_book_matrix.columns.tolist()
    user_book_matrix.fillna(0, inplace=True)
    return [users_list, books_list, user_book_matrix.values]


def encoder(x, weights, biases):
    layer_1 = tf.nn.sigmoid(
        tf.add(tf.matmul(x, weights["encoder_h1"]), biases["encoder_b1"])
    )
    layer_2 = tf.nn.sigmoid(
        tf.add(tf.matmul(layer_1, weights["encoder_h2"]), biases["encoder_b2"])
    )
    return layer_2


def decoder(x, weights, biases):
    layer_1 = tf.nn.sigmoid(
        tf.add(tf.matmul(x, weights["decoder_h1"]), biases["decoder_b1"])
    )
    layer_2 = tf.nn.sigmoid(
        tf.add(tf.matmul(layer_1, weights["decoder_h2"]), biases["decoder_b2"])
    )
    return layer_2


def train_tf_model(users, books, user_book_matrix, combined):
    tf.compat.v1.disable_v2_behavior()
    num_input = combined["Book-Title"].nunique()
    num_hidden_1 = 10
    num_hidden_2 = 5

    X = tf.placeholder(tf.float64, [None, num_input])

    weights = {
        "encoder_h1": tf.Variable(
            tf.random_normal([num_input, num_hidden_1], dtype=tf.float64)
        ),
        "encoder_h2": tf.Variable(
            tf.random_normal([num_hidden_1, num_hidden_2], dtype=tf.float64)
        ),
        "decoder_h1": tf.Variable(
            tf.random_normal([num_hidden_2, num_hidden_1], dtype=tf.float64)
        ),
        "decoder_h2": tf.Variable(
            tf.random_normal([num_hidden_1, num_input], dtype=tf.float64)
        ),
    }

    biases = {
        "encoder_b1": tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
        "encoder_b2": tf.Variable(tf.random_normal([num_hidden_2], dtype=tf.float64)),
        "decoder_b1": tf.Variable(tf.random_normal([num_hidden_1], dtype=tf.float64)),
        "decoder_b2": tf.Variable(tf.random_normal([num_input], dtype=tf.float64)),
    }

    encoder_op = encoder(X, weights, biases)
    decoder_op = decoder(encoder_op, weights, biases)

    y_pred = decoder_op
    y_true = X

    loss = tf.losses.mean_squared_error(y_true, y_pred)
    optimizer = tf.train.RMSPropOptimizer(0.03).minimize(loss)
    eval_x = tf.placeholder(
        tf.int32,
    )
    eval_y = tf.placeholder(
        tf.int32,
    )
    pre, pre_op = tf.metrics.precision(labels=eval_x, predictions=eval_y)

    init = tf.global_variables_initializer()
    local_init = tf.local_variables_initializer()
    pred_data = pd.DataFrame()

    with tf.Session() as session:
        epochs = 100
        batch_size = 35

        session.run(init)
        session.run(local_init)

        num_batches = int(user_book_matrix.shape[0] / batch_size)
        user_book_matrix = np.array_split(user_book_matrix, num_batches)

        for i in range(epochs):
            avg_cost = 0
            for batch in user_book_matrix:
                _, l = session.run([optimizer, loss], feed_dict={X: batch})
                avg_cost += l

            avg_cost /= num_batches

            print("epoch: {} Loss: {}".format(i + 1, avg_cost))

        user_book_matrix = np.concatenate(user_book_matrix, axis=0)

        preds = session.run(decoder_op, feed_dict={X: user_book_matrix})

        pred_data = pd.concat([pred_data, pd.DataFrame(preds)], ignore_index=True)

        pred_data = pred_data.stack().reset_index(name="Book-Rating")
        pred_data.columns = ["User-ID", "Book-Title", "Book-Rating"]
        pred_data["User-ID"] = pred_data["User-ID"].map(lambda value: users[value])
        pred_data["Book-Title"] = pred_data["Book-Title"].map(
            lambda value: books[value]
        )

        keys = ["User-ID", "Book-Title"]
        index_1 = pred_data.set_index(keys).index
        index_2 = combined.set_index(keys).index

        top_ten_ranked = pred_data[~index_1.isin(index_2)]
        top_ten_ranked = top_ten_ranked.sort_values(
            ["User-ID", "Book-Rating"], ascending=[True, False]
        )
        top_ten_ranked = top_ten_ranked.groupby("User-ID").head(10)
    return top_ten_ranked
