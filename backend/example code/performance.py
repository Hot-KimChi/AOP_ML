import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
import time

# MNIST 데이터셋 불러오기
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 데이터 전처리
x_train = x_train.reshape(60000, 28, 28, 1).astype('float32') / 255
x_test = x_test.reshape(10000, 28, 28, 1).astype('float32') / 255

# 모델 정의
model = Sequential([
    Flatten(input_shape=(28, 28, 1)),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# 모델 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 모델 학습 시작 시간 기록
start_time = time.time()

# 모델 학습
model.fit(x_train, y_train, epochs=5, batch_size=128, verbose=1)

# 모델 학습 종료 시간 기록
end_time = time.time()

# 학습 시간 계산
training_time = end_time - start_time
print(f'모델 학습 시간: {training_time:.2f} 초')

# 모델 평가
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 정확도: {test_acc * 100:.2f}%')