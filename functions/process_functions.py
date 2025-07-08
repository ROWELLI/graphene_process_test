import pandas as pd
import math
import os
from config import *

# 공정 input, ouput 관리 알고리즘
# 공정이름, 다음 공정 이름(비율 계산용), 미뤄진 날짜, 전 release에서 ouput 계산값
def processing_logic(stage_name, next_stage_name, day_offset, stage_goal):
    # 열 이름(생산, 양품, 불량품, 불출, 이월재고, 재고)
    columns = ['Produced', 'Pass', 'Fail', 'Released', 'CarryOver', 'Stock']
    data = []

    # 초기 설정
    stock = 0
    day = day_offset
    total_fails = 0

    while True:
        produced = min(stage_goal, processes[stage_name]['throughput'])
        stage_goal -= produced
        failed = math.ceil(produced * processes[stage_name]['reject'])
        passed = produced - failed
        # 불량품 개수 더해서 나중에 계산할 값에 대해서 빼줌
        total_fails += failed
        # 여기 에러 있음 여기 조건문에 안걸리면(delay가 없을시 에러남)
        if day > processes[stage_name]['delay']:
            output = round(processes[next_stage_name]['throughput']//processes[next_stage_name]['ratio']) # 어차피 정수값이라 이렇게 설정
            if stock < output:
                # 정수 물품만 가능하기 때문에 ratio가 1보다 낮은 경우 소수점 처리
                if processes[next_stage_name]['ratio'] < 1:
                    release_multiples = round((1/processes[next_stage_name]['ratio'])*(stock//(1/processes[next_stage_name]['ratio'])))
                    released = max(release_multiples, stock-release_multiples)
                    if released is not release_multiples:
                        total_fails += released
                else:
                    released = stock
            else:
                released = output
        else:
            released = 0
        # 이용 안하고 있는 중
        carry_over = 0
        stock += (passed-released)
        data.append([day, produced, passed, failed, released, carry_over, stock])

        if stage_goal <= 0 and stock == 0: 
            break
        day += 1

    # csv 관리하는 것부터 함수 새로 만드는게 좋을듯

    # 결과 csv파일들을 output폴더 안에 저장

    # csv 파일 생성
    df = pd.DataFrame(data, columns=['Day'] + columns)
    df.set_index('Day', inplace=True)
    # df.to_csv(os.path.join(output_dir, f"{stage_name}.csv"), index_label='Day', encoding='utf-8-sig')

    # 딜레이된 날짜 계산
    # 이후 merge하면서 열 개수 만큼 빼든지 갯수 바꿔야 함
    start_day = df[df['Released'] > 0].index[0]
    print(df.head())
    return df, start_day, total_fails

# 로직은 processing_logic과 유사
def ending_process(stage_name, day_offset, stage_goal):
    columns = ['Produced', 'Pass', 'Fail', 'Released', 'CarryOver', 'Stock']
    data = []

    stock = 0
    day = day_offset
    while True:
        if stage_goal > processes[stage_name]['throughput']:
            produced = processes[stage_name]['throughput']
        else:
            produced = stage_goal
        stage_goal -= produced
        failed = math.ceil(produced * processes[stage_name]['reject'])
        passed = produced - failed

        released = 0
        carry_over = 0
        stock += passed
        data.append([day, produced, passed, failed, released, carry_over, stock])
        
        if stage_goal <= 0: 
            break
        day += 1

    df = pd.DataFrame(data, columns=['Day'] + columns)
    df.set_index('Day', inplace=True)
    # df.to_csv(os.path.join(output_dir, f"{stage_name}.csv"), index_label='Day', encoding='utf-8-sig')
    return df

# def merge_data():   
