import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def draw2d(input_file, output_file, title):
    plt.rcParams['figure.figsize'] = (16, 10)  # 设置更大的图形尺寸
    plt.rcParams['font.size'] = 12  # 增大字体大小
    plt.rcParams['lines.linewidth'] = 2  # 增加线条宽度

    df = pd.read_csv(input_file)

    fig, ax = plt.subplots()

    for stock in df['stocks'].unique():
        subset = df[df['stocks'] == stock]
        ax.plot(subset['years'], subset['time'], marker='o', markersize=8, label=f'Stocks {stock}')

    ax.set_title(f'{title} : Time vs. Years for different Stock Quantity', fontsize=20)
    ax.set_xlabel('Years', fontsize=16)
    ax.set_ylabel('Time', fontsize=16)
    ax.legend(fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')

def draw3d(input_file, output_file, title):
    df = pd.read_csv(input_file)

    # 提取特征和目标变量
    X = df[['stocks', 'years']].values
    y = df['time'].values

    # 使用多项式特征
    poly = PolynomialFeatures(degree=2)  # 可以调整degree的值来增加或减少多项式的复杂度
    X_poly = poly.fit_transform(X)

    # 拟合回归模型
    model = LinearRegression()
    model.fit(X_poly, y)

    # 生成预测数据
    stocks_range = np.linspace(df['stocks'].min(), df['stocks'].max(), 100)
    years_range = np.linspace(df['years'].min(), df['years'].max(), 5) 
    stocks_grid, years_grid = np.meshgrid(stocks_range, years_range)
    X_pred = np.vstack([stocks_grid.ravel(), years_grid.ravel()]).T
    X_pred_poly = poly.transform(X_pred)
    time_pred = model.predict(X_pred_poly)
    time_pred_grid = time_pred.reshape(stocks_grid.shape)

    # 绘制结果
    plt.figure(figsize=(14, 6))

    # 3D折线图
    ax = plt.axes(projection='3d')
    ax.plot_surface(stocks_grid, years_grid, time_pred_grid, cmap='viridis', edgecolor='none')
    ax.set_xlabel('Stocks')
    ax.set_ylabel('Years')
    ax.set_zlabel('Time')
    ax.set_title(f'{title}: Plot of Time vs Stocks and Years')

    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    draw3d('../result/eigen_analysis.csv', '../result/eigen_3d.png', 'Eigen')
    draw3d('../result/pandas_analysis.csv', '../result/pandas_3d.png', 'Pandas')
    draw2d('../result/eigen_analysis.csv', '../result/eigen_2d.png', 'Eigen')
    draw2d('../result/pandas_analysis.csv', '../result/pandas_2d.png', 'Pandas')