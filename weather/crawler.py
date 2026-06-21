#这一部分是数据爬取部分
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class WeatherCrawler:
    def __init__(self):
        self.base_url = "http://www.weather.com.cn"
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "origin": "https://www.weather.com.cn",
            "priority": "u=1, i",
            "referer": "https://www.weather.com.cn/",
            "sec-ch-ua": "\"Chromium\";v=\"9\", \"Not?A_Brand\";v=\"8\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.6.5061 SLBChan/133 SLBVPV/64-bit"
        }

    def get_city_code(self, city_name):
        # 可手动维护或从网络获取城市代码映射,获取城市代码（中国天气网使用城市代码查询）
        city_codes = {
            '洛阳': '101180901',
            '开封': '101180801',
            '北京': '101010100',
            '上海': '101020100',
            '广州': '101280101',
            '深圳': '101280601',
            '杭州': '101210101',
            '南京': '101190101',
            '武汉': '101200101',
            '成都': '101270101',
            '重庆': '101040100',
            '西安': '101110101'
        }
        return city_codes.get(city_name, None)

    def crawl_7day_weather(self, city_name):
        #爬取未来7天天气数据
        city_code = self.get_city_code(city_name)
        if not city_code:
            print(f"未找到{city_name}的城市代码")
            return None
        url = f"{self.base_url}/weather/{city_code}.shtml"

        response = requests.get(url, headers=self.headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        # 解析7天天气预报
        weather_data = []
        days = soup.find('ul', class_='t clearfix').find_all('li')
        for day in days:
            date = day.find('h1').text
            weather = day.find('p', class_='wea').text
            temp = day.find('p', class_='tem')
            high_temp = temp.find('span').text.replace('℃', '')
            low_temp = temp.find('i').text.replace('℃', '')
            wind = day.find('p', class_='win').find('i').text
            weather_data.append({
                '日期': date,
                '城市': city_name,
                '天气': weather,
                '最高温': int(high_temp),
                '最低温': int(low_temp),
                '风力': wind
            })
        df = pd.DataFrame(weather_data)
        return df


    # 保存数据到CSV文件
    def save_to_csv(self, df, filename):
        if df is not None:
            df.to_csv(f"data/raw/{filename}.csv", index=False, encoding='utf-8-sig')
            print(f"数据已保存到 data/raw/{filename}.csv")