#这里是用来分析数据的
import pandas as pd
import numpy as np
from collections import Counter

class WeatherAnalyzer:
    def __init__(self, data):
        self.data = data

    def basic_statistics(self):
        #基础统计分析
        stats = {
            '平均最高温': self.data['最高温'].mean(),
            '平均最低温': self.data['最低温'].mean(),
            '最高温极值': self.data['最高温'].max(),
            '最低温极值': self.data['最低温'].min(),
            '温度标准差': self.data['平均温度'].std(),
            '昼夜温差均值': (self.data['最高温'] - self.data['最低温']).mean()
        }
        return stats

    def weather_frequency(self):
        #天气类型频率分析
        freq = self.data['天气类型'].value_counts()
        return freq

    def temperature_trend(self):
        #温度趋势分析,计算温度变化率（如果有多天数据）
        if len(self.data) > 1:
            self.data = self.data.sort_values('日期')
            self.data['温度变化'] = self.data['平均温度'].diff()
        return self.data

    def get_recommendations(self):
        #根据天气给出建议
        recommendations = []
        avg_temp = self.data['平均温度'].mean()

        if avg_temp > 25:
            recommendations.append("天气较热，建议穿短袖，注意防暑")
        elif avg_temp < 10:
            recommendations.append("天气较冷，建议穿厚外套，注意保暖")
        else:
            recommendations.append("天气舒适，适合户外活动")
        if any('雨' in w for w in self.data['天气']):
            recommendations.append("有雨天，请携带雨具")
        return recommendations