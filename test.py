bream_length = [25.4, 26.3, 26.5, 29.0, 29.0, 29.7, 29.7, 30.0, 30.0, 30.7, 31.0, 31.0, 31.5, 32.0, 32.0, 32.0, 33.0, 33.0, 33.5, 33.5, 34.0, 34.0, 34.5, 35.0, 35.0, 35.0, 35.0, 36.0, 36.0, 37.0, 38.5, 38.5, 39.5, 41.0, 41.0]
bream_weight = [242.0, 290.0, 340.0, 363.0, 430.0, 450.0, 500.0, 390.0, 450.0, 500.0, 475.0, 500.0, 500.0, 340.0, 600.0, 600.0, 700.0, 700.0, 610.0, 650.0, 575.0, 685.0, 620.0, 680.0, 700.0, 725.0, 720.0, 714.0, 850.0, 1000.0, 920.0, 955.0, 925.0, 975.0, 950.0]
smelt_length = [9.8, 10.5, 10.6, 11.0, 11.2, 11.3, 11.8, 11.8, 12.0, 12.2, 12.4, 13.0, 14.3, 15.0]
smelt_weight = [6.7, 7.5, 7.0, 9.7, 9.8, 8.7, 10.0, 9.9, 9.8, 12.2, 13.4, 12.2, 19.7, 19.9]


## 데이터 그리기
import matplotlib.pyplot as plt
plt.scatter(bream_length, bream_weight)
plt.scatter(smelt_length, smelt_weight)
plt.xlabel('length')
plt.ylabel('weight')
plt.show()


## 데이터 가공 --> 2차원 리스트로 만들기
length = bream_length + smelt_length
weight = bream_weight + smelt_weight

fish_data = [[l, w] for l, w in zip(length, weight)]
target = [1]*35 + [0]*14
print(len(fish_data), len(target))
print(fish_data, target)


## 훈련시키기
from sklearn.neighbors import KNeighborsClassifier
kn = KNeighborsClassifier()
kn.fit(fish_data, target)
print(kn.score(fish_data, target))



kn_opt = KNeighborsClassifier()
kn_opt.fit(fish_data, target)

for n in range(5, 35):
    kn_opt.n_neighbors = n
    score = kn_opt.score(fish_data, target)
    if score < 1:
        print(n, score)
        break


## sampling bias 해결 방안.
## 다시 시작하는 Kneighbors
from sklearn.neighbors import KNeighborsClassifier
kn = KNeighborsClassifier()

##
import numpy as np
input_array = np.array(fish_data)
target_array = np.array(target)
print(input_array, target_array)
print(input_array.shape, target_array.shape)


## random 함수로 섞어서 train set와 test set 구분.
index = np.arange(49)
np.random.seed(42)
np.random.shuffle(index)


train_input = input_array[index[:35]]
train_target = target_array[index[:35]]
test_input = input_array[index[35:]]
test_target = target_array[index[35:]]


kn.fit(train_input, train_target)
print(kn.score(train_input, train_target))
print(kn.score(test_input, test_target))
