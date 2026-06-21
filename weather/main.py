#这里是python期末大作业的主程序
from crawler import WeatherCrawler
from cleaner import WeatherCleaner
from analyze import WeatherAnalyzer
from photo import WeatherVisualizer
import pandas as pd
import os

def main():
    print("=" * 50)
    print("       天气数据爬取与可视化分析系统")
    print("=" * 50)
    # 1. 爬取数据
    print("\n[1] 开始爬取天气数据...")
    crawler = WeatherCrawler()
    city = input("请输入城市名称（仅限洛阳，开封，北上广深，杭州，南京，武汉，成都，重庆，西安）: ")

    weather_df = crawler.crawl_7day_weather(city)
    if weather_df is not None:
        crawler.save_to_csv(weather_df, f"{city}_weather_raw")
        print(f"{city}天气数据爬取成功！")
    else:
        print("数据爬取失败，请检查网络或城市名称")
        return
    # 2. 数据清洗
    print("\n[2] 开始清洗数据...")
    cleaner = WeatherCleaner()
    raw_data = cleaner.load_data(f"data/raw/{city}_weather_raw.csv")
    cleaned_data = cleaner.clean_data(raw_data)
    cleaner.save_cleaned_data(cleaned_data, f"{city}_weather_cleaned.csv")
    print("数据清洗完成！")
    # 3. 数据分析
    print("\n[3] 开始数据分析...")
    analyzer = WeatherAnalyzer(cleaned_data)
    stats = analyzer.basic_statistics()
    freq = analyzer.weather_frequency()
    recommendations = analyzer.get_recommendations()
    print("\n分析结果摘要：")
    print(f"平均最高温: {stats['平均最高温']:.1f}℃")
    print(f"平均最低温: {stats['平均最低温']:.1f}℃")
    print(f"昼夜温差均值: {stats['昼夜温差均值']:.1f}℃")
    print(f"\n天气类型频率: \n{freq}")
    print(f"\n生活建议: {', '.join(recommendations)}")
    # 4. 数据可视化
    print("\n[4] 生成可视化图表...")
    visualizer = WeatherVisualizer(cleaned_data)
    # 创建输出目录
    os.makedirs("output/charts", exist_ok=True)
    # 生成各种图表
    visualizer.plot_temperature_trend(f"output/charts/{city}_temperature_trend.png")
    visualizer.plot_weather_distribution(f"output/charts/{city}_weather_dist.png")
    print(f"图表已保存到 output/charts/ 目录")
    # 5. 保存分析报告
    print("\n[5] 生成分析报告...")
    with open(f"output/reports/{city}_天气分析报告.txt", 'w', encoding='utf-8') as f:
        f.write(f"{city}未来7天天气分析报告\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"分析时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("一、基础统计\n")
        for key, value in stats.items():
            f.write(f"  {key}: {value:.2f}\n")
        f.write("\n二、天气类型分布\n")
        for weather, count in freq.items():
            f.write(f"  {weather}: {count}天\n")
        f.write("\n三、生活建议\n")
        for i, rec in enumerate(recommendations, 1):
            f.write(f"  {i}. {rec}\n")
    print(f"分析报告已保存到 output/reports/{city}_天气分析报告.txt")
    print("\n项目执行完成！")

if __name__ == "__main__":
    main()