import numpy as np
import time

def matrix_multiplication(matrix1, matrix2):
    result = np.matmul(matrix1, matrix2)
    return result

# 행렬 크기 설정
matrix_size = 2000

# 큰 행렬 생성
matrix1 = np.random.rand(matrix_size, matrix_size)
matrix2 = np.random.rand(matrix_size, matrix_size)

# 연산 시작 시간 기록
start_time = time.time()

# 행렬 곱셈 수행
result = matrix_multiplication(matrix1, matrix2)

# 연산 종료 시간 기록
end_time = time.time()

# 연산 시간 계산
operation_time = end_time - start_time
print(f"행렬 곱셈 연산 시간: {operation_time:.6f} 초")