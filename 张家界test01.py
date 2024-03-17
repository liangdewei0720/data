# # -*- coding: utf-8 -*-
import csv
import random
import time

import requests
from bs4 import BeautifulSoup
import re


def save_to_csv(data):
    """
    将数据保存到CSV文件中
    :param data: 要保存的数据，格式为列表或元组的列表
    """
    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 如果文件为空，则写入表头
        if file.tell() == 0:
            writer.writerow(['景点名字', '排名', '评分', '链接'])  # 写入表头
        writer.writerows(data)

def extract_links(url):
    """
    从指定URL的网页中提取每个a标签的链接并输出
    :param url: 要爬取的网页URL
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    data = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')
        links = soup.select(
            'body > div.qn_main_box > div > div.qn_main_ct.clrfix > div.qn_main_ct_l > div > div.listbox > ul > li > a')
        if links:
            for link in links:
                href = link.get('href')
                #print(href)
                data.append(href)
        else:
            data.append("无")
            #print("未找到匹配的a标签")
    else:
        print("网页请求失败")
    return data

def extract_last_span_text(url):
    """
    从指定URL的网页中提取指定选择器路径下每个元素最后一个span的文本内容并输出
    :param url: 要爬取的网页URL
    """
    selector = 'body > div.qn_main_box > div > div.qn_main_ct.clrfix > div.qn_main_ct_l > div > div.listbox > ul > li > div > div.txtbox.clrfix > div.countbox > span.total_star > span:last-child'

    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    data = []
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')
        for i in range(1, 11):  # 循环从1到10
            selector = f'body > div.qn_main_box > div > div.qn_main_ct.clrfix > div.qn_main_ct_l > div > div.listbox > ul > li:nth-child({i}) > div > div.txtbox.clrfix > div.countbox > span.total_star > span'
            span = soup.select_one(selector)
            if span:
                style_attr = span['style']
                width_percentage = style_attr.split(':')[1].strip('%;"')
                #print(width_percentage)
                data.append(width_percentage)
            else:
                #print(f"未找到第{i}个选择器对应的元素")
                data.append("无")
    else:
        print("网页请求失败")
    return data

def extract_chinese_text(url):
    """
    从指定URL的网页中提取所有中文文本并输出
    :param url: 要爬取的网页URL
    """
    data = []
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')
        texts = soup.select('div ul li div div a span')
        for text in texts:
            chinese_text = re.sub(r'[^\u4e00-\u9fa5]', '', text.get_text())
            if chinese_text:
                data.append(chinese_text)
            else:
                # 如果 chinese_text 为空，则执行以下操作或者跳过
                pass
    return data

def extract_text(url):
    """
    从指定URL的网页中提取所有文本并输出
    :param url: 要爬取的网页URL
    """
    data = []
    headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_text = response.text
        soup = BeautifulSoup(html_text, 'html.parser')
        countboxes = soup.select(
            'body > div.qn_main_box > div > div.qn_main_ct.clrfix > div.qn_main_ct_l > div > div.listbox > ul > li > div > div.txtbox.clrfix > div.countbox')
        if countboxes:
            for countbox in countboxes:
                ranking_sum = countbox.select_one('span.ranking_sum')
                if ranking_sum:
                    ranking_text = ranking_sum.get_text().strip()
                    if ranking_text:
                        #print(ranking_text)
                        data.append(ranking_text)
                        next_span = ranking_sum.find_next_sibling('span')
                        if next_span:
                            next_text = next_span.get_text().strip()
                            if next_text:
                                print(next_text)
                            else:
                                data.append("无")
                                #print("无")
                    else:
                        data.append("无")
                        #print("无")
                else:
                    data.append("无")
                    #print("无")
        else:
            print("无")
    return data

if __name__ == '__main__':

    base_url = "http://travel.qunar.com/p-cs300064-zhangjiajie-jingdian-1-"
    for i in range(1,50):  # 根据你提供的链接总数确定循环次数
        url = base_url + str(i)
        data = []
        print(f"正在爬取第 {i} 页：{url}")
        # 随机停顿2-7秒
        sleep_time = random.randint(1, 4)
        time.sleep(sleep_time)
        # 提取数据

        chinese_text = extract_chinese_text(url)#景点名字
        text = extract_text(url)#排名
        last_span_text = extract_last_span_text(url)#评分
        links = extract_links(url)#链接
        for i in range(0,10):
            # print(chinese_text[i])
            # print(text[i])
            # print(last_span_text[i])
            # print(links[i])
            #将数据加入到列表中
            data.append((chinese_text[i], text[i], last_span_text[i], links[i]))
        # 保存数据到CSV文件
        save_to_csv(data)
    #extract_chinese_text(url)
    #extract_text(url)
    #extract_last_span_text(url)
    #extract_links(url)