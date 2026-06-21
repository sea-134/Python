#这个模块用来生成各种图的,使用seaborn
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
#颜色列表
colorssell=[ '#FF9999',  # 浅红色
             '#66B2FF',  # 浅蓝色
             '#99FF99',  # 浅绿色
             '#FFCC99',  # 浅橙色
             '#FF99FF',  # 浅紫色
             '#FFFF99',  # 浅黄色
             '#99FFFF',  # 浅青色
             '#CC99FF',  # 浅紫罗兰
]

class WeatherVisualizer:
    def __init__(self, data):
        self.data = data

    def plot_temperature_trend(self, save_path=None):
        #绘制温度趋势图
        plt.figure(figsize=(12, 6))

        # 折线图：最高温和最低温
        plt.plot(self.data['日期'], self.data['最高温'],label='最高温', marker='o', color='red', linewidth=2)
        plt.plot(self.data['日期'], self.data['最低温'],label='最低温', marker='s', color='blue', linewidth=2)
        plt.plot(self.data['日期'], self.data['平均温度'], label='平均温度', marker='^', color='green', linestyle='--')

        # 填充昼夜温差区域
        plt.fill_between(self.data['日期'],self.data['最低温'],self.data['最高温'],color='gray', alpha=0.3)

        plt.title('未来7天温度变化趋势', fontsize=16, fontweight='bold')
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('温度(℃)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

    def plot_weather_distribution(self, save_path=None):
        #绘制天气类型分布图
        plt.figure(figsize=(10, 6))
        weather_counts = self.data['天气类型'].value_counts()
        colors = colorssell[:len(weather_counts)]
        # 饼图
        plt.pie(weather_counts.values, labels=weather_counts.index,
                autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('天气类型分布', fontsize=16, fontweight='bold')
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()