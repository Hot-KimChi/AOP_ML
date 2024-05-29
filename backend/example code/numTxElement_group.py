import pandas as pd

# 예제 데이터프레임 생성 (실제 데이터로 대체 필요)
data = {
    'IsTxChannelModulationEn': [1, 0, 1, 1, 0, 1, 1, 0, 1],
    'ProbeNumTxCycles': [2, 2, 2, 3, 3, 3, 4, 4, 4],
    'SysTxFreqIndex': [3, 3, 3, 3, 3, 3, 4, 4, 4],
    'TxpgWaveformStyle': [4, 4, 4, 4, 4, 4, 5, 5, 5],
    'TxPulseRle': [5, 5, 5, 5, 5, 5, 6, 6, 6],
    'ElevAperIndex': [6, 6, 6, 6, 6, 6, 7, 7, 7],
    'TxFocusLocCm': [7, 7, 7, 7, 7, 7, 8, 8, 8],
    'NumTxElements': [8, 8, 8, 9, 9, 10, 8, 8, 8]
}
df_total_BM = pd.DataFrame(data)

# 빈 리스트를 만들어 그룹 ID를 할당
group_ids = []

# 3개씩 그룹핑하여 그룹 ID 할당
for i in range(len(df_total_BM)):
    group_id = i // 3
    group_ids.append(group_id)

# 그룹 ID를 데이터프레임에 추가
df_total_BM['GroupID'] = group_ids

# 각 그룹별로 NumTxElements 값이 동일한지 확인하여 유효성 판단
def is_group_valid(group):
    return len(set(group['NumTxElements'])) == 1

# 그룹 유효성 검사
df_total_BM['IsGroupValid'] = df_total_BM.groupby('GroupID').apply(is_group_valid).reset_index(drop=True)

# 유효한 그룹과 유효하지 않은 그룹 분리
valid_groups = df_total_BM[df_total_BM['IsGroupValid'] == True]
invalid_groups = df_total_BM[df_total_BM['IsGroupValid'] == False]

# 결과 출력
print("Valid Groups:")
print(valid_groups)
print("\nInvalid Groups:")
print(invalid_groups)
