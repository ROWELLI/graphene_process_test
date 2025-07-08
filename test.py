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



# def processing_logic(stage_name, next_stage_name, day_offset, stage_goal):
#     columns = ['Produced', 'Pass', 'Fail', 'Released', 'CarryOver', 'Stock']
#     data = []

#     # df = pd.DataFrame(columns=columns, index=range(day_offset+1, day_offset + num_days + 1))
#     # df = df.fillna(0)

#     stock = 0
#     day = day_offset
#     while True:
#         if stage_goal > processes[stage_name]['throughput']:
#             produced = processes[stage_name]['throughput']
#         else:
#             produced = stage_goal
#         stage_goal -= produced
#         failed = math.ceil(produced * processes[stage_name]['reject'])
#         passed = produced - failed

#         output = round(processes[next_stage_name]['throughput']//processes[next_stage_name]['ratio']) # 어차피 정수값이라 이렇게 설정
#         # 여기 에러 있음 여기 조건문에 안걸리면(delay가 없을시 에러남)
#         if day > processes[stage_name]['delay']:
#             released = stock if stock < output else output
#         else:
#             released = 0
#         carry_over = 0
#         stock += (passed-released)
#         data.append([day, produced, passed, failed, released, carry_over, stock])
#         # stock -= released
#         # stock = prev_stock + produced - released
#         prev_stock = stock
        
#         if stage_goal <= 0 and stock == 0: 
#             print(day)
#             break
#         day += 1
    
#     df = pd.DataFrame(data, columns=['Day'] + columns)
#     df.set_index('Day', inplace=True)
#     df.to_csv(f"{stage_name}.csv", index_label='Day', encoding='utf-8-sig')
    
#     start_day = df[df['Released'] > 0].index[0]
#     print(df.head())
#     return start_day

# def ending_process(stage_name, day_offset, stage_goal):
#     columns = ['Produced', 'Pass', 'Fail', 'Released', 'CarryOver', 'Stock']
#     data = []

#     # df = pd.DataFrame(columns=columns, index=range(day_offset+1, day_offset + num_days + 1))
#     # df = df.fillna(0)

#     stock = 0
#     day = day_offset
#     while True:
#         if stage_goal > processes[stage_name]['throughput']:
#             produced = processes[stage_name]['throughput']
#         else:
#             produced = stage_goal
#         stage_goal -= produced
#         failed = math.ceil(produced * processes[stage_name]['reject'])
#         passed = produced - failed

#         released = 0
#         carry_over = 0
#         stock += passed
#         data.append([day, produced, passed, failed, released, carry_over, stock])
        
#         if stage_goal <= 0: 
#             break
#         day += 1
    
#     df = pd.DataFrame(data, columns=['Day'] + columns)
#     df.set_index('Day', inplace=True)
#     df.to_csv(f"{stage_name}.csv", index_label='Day', encoding='utf-8-sig')

stage_goal = math.ceil(EQ_product/processes[stage_names[1]]['ratio'])
# print(EQ_product/processes[stage_names[1]]['ratio'], stage_goal)

start_day = 1
for i in range(len(processes)-1):
    stage_goal *= processes[stage_names[i]]['ratio']
    num_days = math.ceil(stage_goal/processes[stage_names[i]]['throughput'])+1
    print(stage_goal, num_days)
    print(start_day)
    start_day = processing_logic(stage_names[i], stage_names[i+1], start_day, stage_goal)

# print(len(processes))
end_stage = stage_names[len(processes)-1]
stage_goal *= processes[end_stage]['ratio']
ending_process(end_stage, start_day, stage_goal)



# start_day = df[df['Released'] > 0].index[0]
# print(f"LAMI 공정 시작일: Day {start_day}")

# 내일 라미 공정일 부터 해보기
# 내생각에는 위에 값 계산하는거 함수로 만들어서 하고 공정마다 전처리 해주면 간단하게 가능
