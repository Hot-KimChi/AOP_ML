import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from functools import partial
import warnings
warnings.filterwarnings("ignore")
import joblib

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


## data load
AOP_data = pd.read_csv('AOP_data.csv')
print(AOP_data.head())

import seaborn as sns
import matplotlib.pyplot as plt

plt.title('distport for zt')
sns.distplot(AOP_data['zt'])
plt.show()

data = AOP_data[['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles',
                 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                 'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm']].to_numpy()
target = AOP_data['zt'].to_numpy()


def DL_DNN(data=None, target=None):
    import tensorflow as tf
    from tensorflow import keras

    train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=0.2)
    from sklearn.preprocessing import StandardScaler

    ss = StandardScaler()
    ss.fit(train_input)
    train_scaled = ss.transform(train_input)
    test_scaled = ss.transform(test_input)

    def func_build_model():
        dense1 = keras.layers.Dense(100, activation='relu', input_shape=(11,), name='hidden')
        dense2 = keras.layers.Dense(10, activation='relu')
        dense3 = keras.layers.Dense(1)

        model = keras.Sequential([dense1, dense2, dense3])

        optimizer = tf.keras.optimizers.RMSprop(0.001)

        model.compile(loss='mse',
                      optimizer=optimizer,
                      metrics=['mae', 'mse'])

        return model


    model = func_build_model()
    print(model.summary())

    ## 10개 sample만 출력하기.
    example_batch = train_scaled[:10]
    example_result = model.predict(example_batch)
    print('example_batch 형태:', example_batch.shape)


    def plot_history(history):
        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch

        plt.figure(figsize=(8, 12))

        plt.subplot(2, 1, 1)
        plt.xlabel('Epoch')
        plt.ylabel('Mean Abs Error [Cm]')
        plt.plot(hist['epoch'], hist['mae'],
                 label='Train Error')
        plt.plot(hist['epoch'], hist['val_mae'],
                 label='Val Error')
        plt.ylim([0, 1.25])
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.xlabel('Epoch')
        plt.ylabel('Mean Square Error [$Cm^2$]')
        plt.plot(hist['epoch'], hist['mse'],
                 label='Train Error')
        plt.plot(hist['epoch'], hist['val_mse'],
                 label='Val Error')
        plt.ylim([0, 2])
        plt.legend()
        plt.show()


    ## 모델 훈련.
    ## 에포크가 끝날 때마다 점(.)을 출력해 훈련 진행 과정을 표시합니다
    class PrintDot(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs):
            if epoch % 100 == 0: print('')
            print('.', end='')


    EPOCHS = 1000

    model = func_build_model()

    # patience 매개변수는 성능 향상을 체크할 에포크 횟수입니다
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
    history = model.fit(train_scaled, train_target, epochs=EPOCHS, validation_split=0.2, verbose=0,
                        callbacks=[early_stop, PrintDot()])

    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch
    print()
    print(hist.tail())

    plot_history(history)

    print('evaluate:', model.evaluate(test_scaled, test_target, verbose=2))
    # loss, mae, mse = model.evaluate(test_scaled, test_target, verbose=2)
    # print("테스트 세트의 평균 절대 오차: {:5.2f} Cm".format(mae))

    ## 테스트 세트에 있는 샘플을 사용해 zt 값을 예측하여 비교하기.
    test_predictions = model.predict(test_scaled).flatten()
    print(test_predictions)
    print(test_target)

    import matplotlib.pyplot as plt

    plt.scatter(test_target, test_predictions)

    plt.xlabel('True Values [Cm]')
    plt.ylabel('Predictions [Cm]')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0, plt.xlim()[1]])
    plt.ylim([0, plt.ylim()[1]])
    _ = plt.plot([-100, 100], [-100, 100])
    plt.show()

    ## 오차의 분표확인.
    error = test_predictions - test_target
    plt.hist(error, bins=25)
    plt.xlabel('Prediction Error [Cm]')
    _ = plt.ylabel('Count')
    plt.show()


def DNN_HonGong(data=None, target=None):
    import tensorflow as tf
    from tensorflow import keras

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=0.2)

    from sklearn.preprocessing import StandardScaler

    # ss = StandardScaler()
    # ss.fit(train_input)
    # train_scaled = ss.transform(train_input)
    # test_scaled = ss.transform(test_input)

    scalerInput = StandardScaler().fit(train_input)
    train_scaled = scalerInput.transform(train_input)
    test_scaled = scalerInput.transform(test_input)

    ## 2D shape 형성로 변경
    train_target = train_target.reshape(-1, 1)
    test_target = test_target.reshape(-1, 1)


    scalerTarget = StandardScaler().fit(train_target)
    train_target_scaled = scalerTarget.transform(train_target)
    test_target_scaled = scalerTarget.transform(test_target)

    # import numpy as np
    # mean = np.mean(train_target, axis=0)
    # std = np.std(train_target, axis=0)
    # print(mean, std)
    # train_target_scaled = (train_target-mean)/std
    # test_target_scaled = (test_target-mean)/std
    # print(train_target_scaled.shape)


    train_scaled, val_scaled, train_target, val_target = train_test_split(train_scaled, train_target_scaled, test_size=0.2)


    def model_fn(a_layer=None):
        model = keras.Sequential()
        model.add(keras.layers.Flatten(input_shape=(11,)))
        model.add(keras.layers.Dense(100, activation='relu', name='hidden'))

        if a_layer:
            model.add(a_layer)

        model.add(keras.layers.Dense(1, name='output'))

        return model


    model = model_fn(keras.layers.Dropout(0.3))
    model.summary()


    rmsprop = keras.optimizers.RMSprop()
    model.compile(optimizer=rmsprop, loss='mse', metrics=['mae', 'mse'])
    # history = model.fit(train_scaled, train_target, epochs=100, validation_data=(val_scaled, val_target))
    checkpoint_cb = keras.callbacks.ModelCheckpoint('best-model.h5')
    early_stopping_cb = keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)


    history = model.fit(train_scaled, train_target, epochs=200, validation_split=0.2,
                        callbacks=[checkpoint_cb, early_stopping_cb])
    print()
    print('num of early_stopping:', early_stopping_cb.stopped_epoch)


    import matplotlib.pyplot as plt
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(['train', 'val'])
    plt.show()

    plt.plot(history.history['mae'])
    plt.plot(history.history['val_mae'])
    plt.xlabel('epoch')
    plt.ylabel('mae')
    plt.legend(['train', 'val'])
    plt.show()


    model = keras.models.load_model('best-model.h5')
    print()
    print('<test evaluate>')
    print('test evaluate:', model.evaluate(test_scaled, test_target_scaled))


    test_label = model.predict(test_scaled)
    test_label = scalerTarget.inverse_transform(test_label)
    print('모양:', test_label.shape, test_target.shape)

    df = pd.DataFrame(x for x in zip(test_label, test_target))

    print()
    print('<csv 추출>')
    df.to_csv('test_est.csv')


if __name__ == '__main__':
    # DL_DNN(data=data, target=target)
    DNN_HonGong(data=data, target=target)