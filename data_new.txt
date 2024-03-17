import csv
import random
import re

import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup


def save_to_csv(data):
    """
    将数据保存到CSV文件中
    :param data: 要保存的数据，格式为列表或元组的列表
    """
    with open('data_1.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 如果文件为空，则写入表头
        if file.tell() == 0:
            writer.writerow(['景点名字', '介绍', '价格', '地址','电话','开放时间'])  # 写入表头
        writer.writerows(data)


def get_links_from_database():
    host = "localhost"
    user = "root"
    password = "root"
    database = "test"

    # 连接到MySQL数据库
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )

    # 创建游标对象
    cursor = conn.cursor()

    try:
        # 执行SQL查询
        cursor.execute("SELECT 链接 FROM data")

        # 从游标中获取所有结果
        results = cursor.fetchall()
        print(results)
        # 将结果保存到数组中
        links = [row['链接'] for row in results]
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

    # 返回链接字段的数组
    return links


def extract_chinese_text(url):
    """
    从指定URL的网页中提取所有中文文本并输出
    :param url: 要爬取的网页URL
    """
    # 设置 Selenium 的 Chrome 选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 运行无头模式
    # 设置 Selenium 的 Chrome 服务
    service = Service(executable_path='F:/python/chromedriver.exe')  # 替换为你的 chromedriver 路径
    # 初始化 Selenium 的 WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # 打开网页
    driver.get(url)
    # 等待页面加载
    time.sleep(3)  # 根据实际情况调整等待时间
    # 获取网页源代码
    html = driver.page_source
    # 关闭 Selenium 的 WebDriver
    driver.quit()
    soup1 = BeautifulSoup(html, 'html.parser')

    data = []
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')


        texts = soup.select('div div h1.tit')
        for text in texts:
            chinese_text = re.sub(r'[^\u4e00-\u9fa5]', '', text.get_text())
            if chinese_text:
                print(chinese_text)
                data.append(chinese_text)
            else:
                # 如果 chinese_text 为空，则执行以下操作或者跳过
                data.append("null")



        jieshao = soup.select("div p.inset-p")
        if jieshao:
            jieshao_all = ""
            for text in jieshao:
                jieshao_text = text.get_text()
                jieshao_all = jieshao_all+jieshao_text
            print(jieshao_all)
            data.append(jieshao_all)
        else :
            jieshao = soup.select("#gs div.e_db_content_box p:first-of-type")
            if jieshao:
                for text in jieshao:
                    jieshao_text = text.get_text()
                    print(jieshao_text)
                    data.append(jieshao_text)
            else:
                print("jieshao_null")
                data.append("null")


        menpaio = soup.select("#mp > div.e_db_content_box.e_db_content_dont_indent > p")
        if menpaio:
            for text in menpaio:
                menpiao_text = text.get_text()
                print(menpiao_text)
                data.append(menpiao_text)
        else:
            print("menpaio_null")
            data.append("null")


        # 使用 BeautifulSoup 的 select 方法选择元素
        dizi = soup1.select(
            '#gs > div.e_summary_list_box.m_summary_two_col > div > table > tbody > tr > td.td_l > dl:nth-child(1) > dd > span')
        # 检查是否找到了元素
        if dizi:
            for text in dizi:
                dizi_text = text.get_text()
                print(dizi_text)
                data.append(dizi_text)
        else:
            dizi1 = soup1.select(
                '#gs > div.e_summary_list_box > div > table > tbody > tr > td.td_l > dl:nth-child(1) > dd > span')
            if dizi1:
                for text in dizi1:
                    dizi_text = text.get_text()
                    print(dizi_text)
                    data.append(dizi_text)
            else:
                print("dizi_null")
                data.append("null")


        dianhua = soup1.select(
            '#gs > div.e_summary_list_box.m_summary_two_col > div > table > tbody > tr > td.td_l > dl:nth-child(2) > dd > span')
        # 检查是否找到了元素
        if dianhua:
            for text in dianhua:
                dianhua_text = text.get_text()
                print(dianhua_text)
                data.append(dianhua_text)
        else:
            dianhua1 = soup1.select(
                '#gs > div.e_summary_list_box.m_summary_two_col > div > table > tbody > tr > td.td_l > dl:nth-child(2) > dd > span')
            if dianhua1:
                for text in dianhua1:
                    dianhua_text = text.get_text()
                    print(dianhua_text)
                    data.append(dianhua_text)
            else:
                print("dianhua_null")
                data.append("null")

        kaifangshijian = soup1.select(
            '#gs > div.e_summary_list_box.m_summary_two_col > div > table > tbody > tr > td.td_r > dl > dd > span > p')
        # 检查是否找到了元素
        if kaifangshijian:
            for text in kaifangshijian:
                kaifangshijian_text = text.get_text()
                print(kaifangshijian_text)
                data.append(kaifangshijian_text)
        else:
            kaifangshijian1 = soup1.select(
                '#gs > div.e_summary_list_box.m_summary_two_col > div > table > tbody > tr > td.td_r > dl > dd > span > p')
            # 检查是否找到了元素
            if kaifangshijian1:
                for text in kaifangshijian1:
                    kaifangshijian_text = text.get_text()
                    print(kaifangshijian_text)
                    data.append(kaifangshijian_text)
            else:
                print("kaifangshijian_null")
                data.append("null")

    return data




if __name__ == "__main__":
    k = 1
    links = get_links_from_database()
    for i in links:
        data_2 = []
        data = extract_chinese_text(i)
        data_2.append((data[0],data[1],data[2],data[3],data[4],data[5]))
        print("第",k,"个，正在爬取：",i,"网站")
        k = k + 1
        save_to_csv(data_2)
        sleep_time = random.randint(1, 4)
        time.sleep(sleep_time)
    # html_content = get_page_content(url)
    # if html_content:
    #     data = extract_data(html_content)
    #     print(data)
