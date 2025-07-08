import config
import pandas as pd
import math
import os


processes = {
    'COMPOSITING': config.COMPOSITING,
    'LAMI': config.LAMI,
    'LQ_INSPECTION': config.LQ_INSPECTION,
    'ETCHING': config.ETCHING,
    'EQ_INSPECTION': config.EQ_INSPECTION,
    'TRANSCRIPTION': config.TRANSCRIPTION
}


def processing_logic(stage_name, next_stage_name, day_offset, stage_goal):
    columns = ['Produced', 'Pass', 'Fail', 'Released', 'CarryOver', 'Stock']
    data = []

    # df = pd.DataFrame(columns=columns, index=range(day_offset+1, day_offset + num_days + 1))
    # df = df.fillna(0)

    stock = 0
    day = day_offset
    while True:
        produced = min(stage_goal, processes[stage_name]['throughput'])
        stage_goal -= produced
        failed = math.ceil(produced * processes[stage_name]['reject'])
        passed = produced - failed

        output = round(processes[next_stage_name]['throughput']//processes[next_stage_name]['ratio']) # 어차피 정수값이라 이렇게 설정
        # 여기 에러 있음 여기 조건문에 안걸리면(delay가 없을시 에러남)
        if day > processes[stage_name]['delay']:
            released = stock if stock < output else output
        else:
            released = 0
        carry_over = 0
        stock += (passed-released)
        data.append([day, produced, passed, failed, released, carry_over, stock])
        # stock -= released
        # stock = prev_stock + produced - released
        prev_stock = stock
        
        if stage_goal <= 0 and stock == 0: 
            print(day)
            break
        day += 1
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(data, columns=['Day'] + columns)
    df.set_index('Day', inplace=True)
    df.to_csv(os.path.join(output_dir, f"{stage_name}.csv"), index_label='Day', encoding='utf-8-sig')
    
    start_day = df[df['Released'] > 0].index[0]
    print(df.head())
    return start_day

def ending_process(stage_name, day_offset, stage_goal):
    columns = ['Produced', 'Pass', 'Fail', 'Released', 'CarryOver', 'Stock']
    data = []

    # df = pd.DataFrame(columns=columns, index=range(day_offset+1, day_offset + num_days + 1))
    # df = df.fillna(0)

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
    
    # df = pd.DataFrame(data, columns=['Day'] + columns)
    # df.set_index('Day', inplace=True)
    # df.to_csv(f"{stage_name}.csv", index_label='Day', encoding='utf-8-sig')

    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame(data, columns=['Day'] + columns)
    df.set_index('Day', inplace=True)
    df.to_csv(os.path.join(output_dir, f"{stage_name}.csv"), index_label='Day', encoding='utf-8-sig')
