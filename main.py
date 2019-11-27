from itertools import islice

import pydotplus
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier, export_text, _tree
from sklearn import tree
import dataprovider
import ta


def tree_to_code(tree_model, feature_names):
    tree_ = tree_model.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)


def load_data(exchange, symbol):
    return dataprovider \
        .DataProvider('nasdaqTradedCompanies.jsonl') \
        .get_company(exchange, symbol) \
        .get_dataframe()


def add_prediction_labels(data_frame):
    buy_pred = []
    sell_pred = []

    for i, cur_price in enumerate(data_frame.Close):
        buy_label = 0
        sell_label = 0

        days_ahead = 5
        # if len(data_frame.Close) > i + days_ahead:
        #     future_price = data_frame.Close[i + days_ahead]
        #     if future_price / cur_price > 1.01:
        #         buy_label = 1
        #     if future_price / cur_price < 0.99:
        #         sell_label = 1

        for future_price in islice(data_frame.Close, i + 1, i + days_ahead):
            if future_price / cur_price > 1.05:
                buy_label = 1
                break
            if future_price / cur_price < 0.98:
                sell_label = 1
                break

        buy_pred.append(buy_label)
        sell_pred.append(sell_label)

    data_frame['buy_label'] = buy_pred
    data_frame['sell_label'] = sell_pred
    return data_frame

def split_last(df, number):
    first = df[:len(df) - number]
    last = df[-1 * number:]
    return first, last


def generate_tree(label, x_train, x_test, y_train, y_test, feature_names):
    buy_tree = DecisionTreeClassifier(max_depth=3)
    buy_tree = buy_tree.fit(x_train, y_train)
    y_pred = buy_tree.predict(x_test)

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # tree_to_code(buy_tree, feature_names=feature_cols)

    text_tree = export_text(buy_tree, feature_names=feature_names, show_weights=True)
    print(text_tree)

    dot_data = tree.export_graphviz(buy_tree, out_file=None, feature_names=feature_names, class_names=["0", "1"], filled=True,
                                    rounded=True, special_characters=True)

    pydotplus.graph_from_dot_data(dot_data).write_png(label + '.png')


def main():
    symbol = "DXLG"
    exchange = "NASDAQ"
    df = load_data("NASDAQ", "DXLG")

    df = ta.add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
    df = add_prediction_labels(df)

    feature_cols = df.columns.values.tolist()
    columns_to_strip = ["buy_label", "sell_label", "DateTime", "CompanyName", "Industry", "Sector", "Exchange", "Symbol", "Open", "Close", "High", "Low", "Volume"]
    for column_name in columns_to_strip:
        feature_cols.remove(column_name)

    # X_train, x_test, y_train, y_test = train_test_split(df[feature_cols], df.sell_label, test_size=0.4, random_state=1)  # 70% training and 30% test

    hold_out_rows = 600
    x_train, x_test = split_last(df[feature_cols], hold_out_rows)
    y_train_buy, y_test_buy = split_last(df.buy_label, hold_out_rows)
    y_train_sell, y_test_sell = split_last(df.sell_label, hold_out_rows)

    print(exchange + ":" + symbol)
    print("Buy Tree")
    generate_tree("buyTree", x_train, x_test, y_train_buy, y_test_buy, feature_cols)
    print("Sell Tree")
    generate_tree("sellTree", x_train, x_test, y_train_sell, y_test_sell, feature_cols)


if __name__ == '__main__':
    main()
