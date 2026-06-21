#数据清洗模块，主要是处理错误的或者格式比较奇怪的数据
import pandas as pd
import numpy as np

class WeatherCleaner:
    def __init__(self):
        pass
    def load_data(self, filepath):
        #加载原始数据
        return pd.read_csv(filepath, encoding='utf-8-sig')
    def clean_data(self, df):
        # 1. 处理缺失值
        df = df.dropna()  # 删除缺失值
        # 2. 处理异常温度值（假设温度在-50到50之间）
        df = df[(df['最高温'] >= -50) & (df['最高温'] <= 50)]
        df = df[(df['最低温'] >= -50) & (df['最低温'] <= 50)]
        # 3. 确保最高温 > 最低温
        df = df[df['最高温'] >= df['最低温']]
        # 4. 计算平均温度
        df['平均温度'] = (df['最高温'] + df['最低温']) / 2
        # 5. 格式化日期，因为原网站上日期格式有点奇怪，这里只给日不给月
        df['日期'] = pd.to_datetime(df['日期'].str.extract(r'(\d{1,2}日)')[0],
                                    format='%d日', errors='coerce')
        df['日期']=df['日期'].dt.day
        # 6. 天气类型分类
        weather_types = ['晴', '多云', '阴', '雨', '雪']
        df['天气类型'] = df['天气'].apply(lambda x: self.classify_weather(x, weather_types))
        return df

    def classify_weather(self, weather_str, types):
        #分类天气类型
        for weather_type in types:
            if weather_type in weather_str:
                return weather_type
        return '其他'

    def save_cleaned_data(self, df, filename):
        #保存清洗后的数据
        df.to_csv(f"data/cleaned/{filename}", index=False, encoding='utf-8-sig')