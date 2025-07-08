import config
import pandas as pd
import math
from functions.process_functions import processing_logic, ending_process
from config import *

# 생산되는 개수
product_count = 1200

stage_names = list(processes)

# 역으로 계산해서 구리개수 산출
EQ_product = product_count/config.TRANSCRIPTION['ratio']
stage_goal = math.ceil(EQ_product/processes[stage_names[1]]['ratio'])

start_day = 1
rejects = 0

# 공정 과정 처리
for i in range(len(processes)-1):
    stage_goal -= rejects
    stage_goal *= processes[stage_names[i]]['ratio']
    print(stage_goal)
    start_day, rejects = processing_logic(stage_names[i], stage_names[i+1], start_day, stage_goal)

end_stage = stage_names[-1]
stage_goal -= rejects
stage_goal *= processes[end_stage]['ratio']
ending_process(end_stage, start_day, stage_goal)
