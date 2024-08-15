import pandas as pd
from itertools import product
from tqdm import tqdm
import time

# 计算加权收益
def calc_weighted_profit(df):
    df['weighted_profit'] = df['profit'] * df['weight']
    weighted_profit_df = df.groupby('date')['weighted_profit'].sum().reset_index()
    return weighted_profit_df

if __name__ == '__main__':
    nums = ['500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '5000']
    years = [('1', '2020'), ('2', '2021'), ('3', '2022'), ('4', '2023'), ('5', '2024')]
    analysis_results = [] 
    total_tasks = len(nums) * len(years)
    
    for num, (year, end_year) in tqdm(product(nums, years), total=total_tasks, desc="Processing"):
        end_date = f"{end_year}-03-01"
        df = pd.read_csv(f'../data/stocks_n{num}_y{year}.csv') 
        
        # 计算加权收益
        start_time = time.time()
        weighted_profit_df = calc_weighted_profit(df)
        end_time = time.time()
        
        weighted_profit_df.to_csv(f'../data/p_weighted_profit_n{num}_y{year}.csv', index=False)
        analysis_results.append({
            'stocks': num,
            'years': year,
            'time': end_time - start_time
        })

    analysis_df = pd.DataFrame(analysis_results)
    analysis_df.to_csv('../result/pandas_analysis.csv', index=False)

