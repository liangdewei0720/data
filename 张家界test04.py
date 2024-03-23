import time
import random
import requests
import csv
from bs4 import BeautifulSoup

def extract_comments(url):
    """
    从指定URL的网页中提取评论内容和日期信息并输出
    :param url: 要爬取的网页URL
    """
    # 打开 CSV 文件准备写入数据
    with open('data_message2.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['评论内容', '日期'])

        # 循环爬取每一页的评论
        for page in range(503, 510):
            # 生成随机睡眠时间
            print(page)
            sleep_time = random.uniform(1, 4)
            time.sleep(sleep_time)

            page_url = f"{url}-{page}?rank=0#lydp"

            # 发送HTTP请求
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(page_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # 使用CSS选择器选择评论内容和日期信息
            comment_contents = soup.select('.e_comment_content')
            comment_dates = soup.select('.e_comment_add_info > ul > li:nth-child(1)')

            # 将评论内容和日期信息写入 CSV 文件
            for content, date in zip(comment_contents, comment_dates):
                writer.writerow([content.get_text(strip=True), date.get_text(strip=True)])
                print(f"评论 内容: {content.get_text(strip=True)}")
                print(f"评论 日期: {date.get_text(strip=True)}")
                print()

if __name__ == "__main__":
    # url = "http://travel.qunar.com/p-oi715200-wulingyuan-1"
    url = "https://travel.qunar.com/p-oi716034-tianmenshanguojiasenlin-1"
    extract_comments(url)
