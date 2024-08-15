import pandas as pd
import numpy as np
from toolkit import selector
from itertools import product
from tqdm import tqdm
import warnings

# 忽略pandas不同版本的警告
warnings.simplefilter(action='ignore', category=DeprecationWarning)

# 从数据库中获取数据并保存到csv文件
def get_all_data(output_file):
    all = selector.select_bars_sql("select ths_code, date, open, close from stock_daily_quotes_non_ror order by date")
    all.to_csv(output_file, index=False)
    return all

# 计算收益率并保存到新的一列
def calc_profit(df):
    df['profit'] = (df['close'] - df['open']) / df['open']
    return df

# 对某组（日期）的股票随机分配权重（总和为1）
def assign_random_weights(group):
    num_stocks = len(group)
    group['weight'] = np.random.rand(num_stocks)
    group['weight'] /= group['weight'].sum()  # 归一化权重
    return group

# 生成权重并保存到新的一列
def generate_weight(df):
    grouped = df.groupby('date')
    weights_df = grouped.apply(assign_random_weights).reset_index(drop=True)
    return weights_df

if __name__ == '__main__':
    nums = ['500', '1000', '1500', '2000', '2500', '3000', '3500', '4000', '4500', '5000']
    years = [('1', '2020'), ('2', '2021'), ('3', '2022'), ('4', '2023'), ('5', '2024')]
    total_tasks = len(nums) * len(years)

    df = get_all_data('../data/stocks.csv')
    df['date'] = pd.to_datetime(df['date'])
    id = df['ths_code'].drop_duplicates()

    for num, (year, end_year) in tqdm(product(nums, years), total=total_tasks, desc="Processing"):
        end_date = f"{end_year}-03-01"
        target_df = df.loc[(df['date']<=end_date) & (df['ths_code'].isin(id.head(int(num))))]
        target_df = generate_weight(target_df)
        target_df = calc_profit(target_df)
        target_df.to_csv(f'../data/stocks_n{num}_y{year}.csv', index=False)