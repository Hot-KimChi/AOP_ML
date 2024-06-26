from sklearn.model_selection import train_test_split


def dataSplit(data, target):
    train_input, test_input, train_target, test_target = train_test_split(
        data, target, test_size=0.2
    )
    return train_input, test_input, train_target, test_target
