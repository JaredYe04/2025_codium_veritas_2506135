from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import numpy as np
import threading
import warnings

# 禁用特定的警告
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

# 加载数据
athlete_log = pd.read_csv('./data/summerOly_athletes.csv')
host = pd.read_csv('./data/hosts.csv')
NOCmap = pd.read_csv('./data/noc_region.csv')
medal_trend = pd.read_csv('./data/predict_medal_trend.csv')
athlete_trend = pd.read_csv('./data/predict_athlete_number_variation.csv')
advantage = pd.read_csv('./data/country_adeptness.csv')
level = pd.read_csv('./data/country_level.csv')
medal_count = pd.read_csv('./data/predict_medal_counts.csv')
participant_count = pd.read_csv('./data/predict_participants.csv')
athlete_args = pd.read_csv('./data/athlete_args.csv')

# 输出文件名
export_filename = './data/train_data.csv'

# 创建线程锁，保证文件操作的线程安全
file_lock = threading.Lock()

def code_2_name(code):
    result = NOCmap[NOCmap['NOC'] == code]['Country'].values[0]
    if result is None:
        print('无法映射' + code)
        return '未知'
    return result

def name_2_code(name):
    result = NOCmap[NOCmap['Country'] == name]['NOC'].values[0]
    if result is None:
        print('无法映射' + name)
        return '未知'
    return result

def process_country(country, country_idx, total_countries):
    print(f'正在处理第{country_idx}个国家，代码为{country}，共{total_countries}个国家')
    terms = participant_count[participant_count['NOC'] == country]['Sport'].values
    years = participant_count[participant_count['NOC'] == country]['Year'].values
    terms = list(set(terms))
    years = list(set(years))
    this_noc = code_2_name(country)
    
    country_data = []
    for term in terms:
        print(f'正在处理第{terms.index(term)+1}个项目，共{len(terms)}个项目')
        for year in years:
            athletes = athlete_log[athlete_log['NOC'] == country][athlete_log['Sport'] == term][athlete_log['Year'] == year]['Name'].values
            for athlete in athletes:
                athlete_arg = athlete_args[athlete_args['Name'] == athlete][['Gold_prob', 'Silver_prob', 'Bronze_prob', 'No_medal_prob']]
                host_arg = host[host['Year'] == year]
                host_noc = name_2_code(host_arg['Host'].values[0])
                is_host_arg = 1.0 if this_noc == host_noc else 0.0
                medal_trend_arg = medal_trend[medal_trend['Sport'] == term][str(year)]
                if medal_trend_arg.empty:
                    medal_trend_arg = 0
                else:
                    medal_trend_arg = medal_trend_arg.values[0]
                athlete_trend_arg = athlete_trend[athlete_trend['Sport'] == term][athlete_trend['Year'] == year][athlete_trend['NOC'] == country]['New']
                athlete_trend_arg = float(athlete_trend_arg) if athlete_trend_arg.size != 0 else 0
                dmedel_dathlete_arg = medal_trend_arg / athlete_trend_arg if athlete_trend_arg != 0 else 0
                advantage_arg = float(advantage[advantage['Sport'] == term][advantage['NOC'] == country]['Adeptness'])
                level_arg = float(level[level['NOC'] == code_2_name(country)]['level'].values[0])

                if level_arg == 5:
                    dmedel_dathlete_arg *= 2
                
                medal_count_arg = medal_count[medal_count['Sport'] == term][str(year)]

                # 检查是否为空，如果为空则设置为0
                if medal_count_arg.empty:
                    medal_count_arg = 0
                else:
                    medal_count_arg = float(medal_count_arg.values[0])
                participant_count_arg = participant_count[participant_count['Sport'] == term][participant_count['Year'] == year][participant_count['NOC'] == country]['Athletes']

                # 检查是否为空，如果为空则设置为0
                if participant_count_arg.empty:
                    participant_count_arg = 0
                else:
                    participant_count_arg = float(participant_count_arg.values[0])
                win_likely_arg = medal_count_arg / participant_count_arg if participant_count_arg != 0 else 0

                country_arg = pd.Series([is_host_arg, dmedel_dathlete_arg, advantage_arg, level_arg, win_likely_arg])
                athlete_arg = pd.Series(athlete_arg.values[0])
                arg = pd.concat([country_arg, athlete_arg], axis=0)

                y = athlete_log[athlete_log['NOC'] == country][athlete_log['Sport'] == term][athlete_log['Year'] == year][athlete_log['Name'] == athlete]['Medal'].values
                gold, silver, bronze = 0, 0, 0
                for i in y:
                    if i == 'Gold':
                        gold += 1
                    elif i == 'Silver':
                        silver += 1
                    elif i == 'Bronze':
                        bronze += 1
                y = [gold, silver, bronze]
                
                country_data.append((arg, y))
    
    # 将处理的结果写入文件
    with file_lock:
        with open(export_filename, 'a') as f:
            for data in country_data:
                f.write(','.join([str(i) for i in data[0]]) + ',' + ','.join([str(i) for i in data[1]]) + '\n')

def main():
    # 写入列名
    with open(export_filename, 'w') as f:
        f.write('is_host_arg,dmedel_dathlete_arg,advantage_arg,level_arg,win_likely_arg,Gold_prob,Silver_prob,Bronze_prob,No_medal_prob,Gold,Silver,Bronze\n')
    
    # 获取国家列表
    country_list = athlete_log['NOC'].unique()
    
    # 使用进程池并行处理每个国家的数据
    from os import cpu_count
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        futures = [executor.submit(process_country, country, idx+1, len(country_list)) for idx, country in enumerate(country_list)]
        
        # 等待所有任务完成
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(e)
                # 如果有异常，打印异常信息，继续处理下一个国家

if __name__ == '__main__':
    main()
