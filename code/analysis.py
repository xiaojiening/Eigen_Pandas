import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (16, 10)  # 设置更大的图形尺寸
plt.rcParams['font.size'] = 12  # 增大字体大小
plt.rcParams['lines.linewidth'] = 2  # 增加线条宽度

##################################################### Pandas #####################################################

df_pandas = pd.read_csv('../result/pandas_analysis.csv')

fig, ax = plt.subplots()

for stock in df_pandas['stocks'].unique():
    subset = df_pandas[df_pandas['stocks'] == stock]
    ax.plot(subset['years'], subset['time'], marker='o', markersize=8, label=f'Stocks {stock}')

ax.set_title('Pandas : Time vs. Years for different Stock Quantity', fontsize=20)
ax.set_xlabel('Years', fontsize=16)
ax.set_ylabel('Time', fontsize=16)
ax.legend(fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('../result/pandas_plot.png', format='png', dpi=300, bbox_inches='tight')

##################################################### Eigen #####################################################

df_eigen = pd.read_csv('../result/eigen_analysis.csv')

fig, ax = plt.subplots()

for stock in df_eigen['stocks'].unique():
    subset = df_eigen[df_eigen['stocks'] == stock]
    ax.plot(subset['years'], subset['time'], marker='o', markersize=8, label=f'Stocks {stock}')

ax.set_title('Eigen : Time vs. Years for different Stock Quantity', fontsize=20)
ax.set_xlabel('Years', fontsize=16)
ax.set_ylabel('Time', fontsize=16)
ax.legend(fontsize=12)
ax.tick_params(axis='both', which='major', labelsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('../result/eigen_plot.png', format='png', dpi=300, bbox_inches='tight')

##################################################### Pandas Vs Eigen #####################################################

df_pandas['Source'] = 'Pandas'
df_eigen['Source'] = 'Eigen'
df_combined = pd.concat([df_pandas, df_eigen])
markers = {'Pandas': 'o', 'Eigen': 's'}  # 圆圈和方块

fig, ax = plt.subplots()

for stock in df_combined['stocks'].unique():
    subset = df_combined[df_combined['stocks'] == stock]
    for source in subset['Source'].unique():
        source_subset = subset[subset['Source'] == source]
        ax.plot(source_subset['years'], source_subset['time'], marker=markers[source], markersize=8, label=f'{source} Stock {stock}')

ax.set_title('Pandas vs. Eigen : Time vs. Years for different Stock Quantity', fontsize=20)
ax.set_xlabel('Years', fontsize=16)
ax.set_ylabel('Time', fontsize=16)
ax.legend(fontsize=12, bbox_to_anchor=(1.05, 1), loc='upper left')
ax.tick_params(axis='both', which='major', labelsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('../result/pandas_vs_eigen_plot.png', format='png', dpi=300, bbox_inches='tight')