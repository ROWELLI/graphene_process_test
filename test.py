import config
import pandas as pd
import math
from functions.process_functions import processing_logic, ending_process
from config import *
import os

# 생산되는 개수
product_count = 2000
stage_names = list(processes)

# 역으로 계산해서 구리개수 산출
EQ_product = product_count/config.TRANSCRIPTION['ratio']
stage_goal = math.ceil(EQ_product/processes[stage_names[1]]['ratio'])

start_day = 1
rejects = 0
final_df = pd.DataFrame()

# 공정 과정 처리
for i in range(len(processes)-1):
    stage_goal -= rejects
    stage_goal *= processes[stage_names[i]]['ratio']
    # print(stage_goal)
    df, start_day, rejects = processing_logic(stage_names[i], stage_names[i+1], start_day, stage_goal)
    df = df.add_prefix(f'{stage_names[i]}_')
    df.index.name = 'Day'
    df.reset_index(inplace=True)

    if final_df.empty:
        final_df = df
    else:
        final_df = pd.merge(final_df, df, on='Day', how='outer')

end_stage = stage_names[-1]
stage_goal -= rejects
stage_goal *= processes[end_stage]['ratio']
df = ending_process(end_stage, start_day, stage_goal)

# 공정 구분하기 위해 열에 공정 이름 붙이기
df = df.add_prefix(f'{end_stage}_')
df.index.name = 'Day'
# Day를 열로 처리
df.reset_index(inplace=True)

# panads.merge() 두개의 테이블 하나로 합치는 함수
# Day 기준으로 합치기 outer로 합침(빈공간 살림)
final_df = pd.merge(final_df, df, on='Day', how='outer')

final_df.sort_values('Day', inplace=True)

output_dir = config.OUTPUT_LOCATON
os.makedirs(output_dir, exist_ok=True)
final_df.to_csv(os.path.join(output_dir, "final_output.csv"), index=False, encoding='utf-8-sig')
