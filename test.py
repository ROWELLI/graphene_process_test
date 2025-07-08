# EQ_product = product_count/config.TRANSCRIPTION['ratio']/(1-config.EQ_INSPECTION['reject'])
# LQ_product = EQ_product/(1-config.EQ_INSPECTION['reject'])
# print(LQ_product, EQ_product)

import config
import pandas as pd
import math
from functions.process_functions import processing_logic, ending_process
product_count = 1200

processes = {
    'COMPOSITING': config.COMPOSITING,
    'LAMI': config.LAMI,
    'LQ_INSPECTION': config.LQ_INSPECTION,
    'ETCHING': config.ETCHING,
    'EQ_INSPECTION': config.EQ_INSPECTION,
    'TRANSCRIPTION': config.TRANSCRIPTION
}
stage_names = list(processes)

EQ_product = product_count/config.TRANSCRIPTION['ratio']

stage_goal = math.ceil(EQ_product/processes[stage_names[1]]['ratio'])
# print(EQ_product/processes[stage_names[1]]['ratio'], stage_goal)

start_day = 1
rejects = 0
for i in range(len(processes)-1):
    stage_goal -= rejects
    stage_goal *= processes[stage_names[i]]['ratio']
    num_days = math.ceil(stage_goal/processes[stage_names[i]]['throughput'])+1
    print(stage_goal, num_days)
    print(start_day)
    start_day, rejects = processing_logic(stage_names[i], stage_names[i+1], start_day, stage_goal)
    print(start_day, rejects)
# print(len(processes))
end_stage = stage_names[len(processes)-1]
stage_goal *= processes[end_stage]['ratio']
ending_process(end_stage, start_day, stage_goal)



# start_day = df[df['Released'] > 0].index[0]
# print(f"LAMI 공정 시작일: Day {start_day}")

# 내일 라미 공정일 부터 해보기
# 내생각에는 위에 값 계산하는거 함수로 만들어서 하고 공정마다 전처리 해주면 간단하게 가능
