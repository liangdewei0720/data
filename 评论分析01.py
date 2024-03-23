# -*- coding: utf-8 -*-
import pymysql
from gensim import corpora, models
import re



# 连接数据库
def connect_db():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 database='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


# 存储主题模型结果到数据库
def save_to_database(lda_model):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 删除现有数据
            cursor.execute("TRUNCATE TABLE topic_modeling_results")

            # 插入新数据
            for topic_id, topic in lda_model.print_topics(-1):
                topic_id = topic_id + 1
                words = filter_chinese_and_punctuation(topic)
                sql = "INSERT INTO topic_modeling_results (topic_id, words) VALUES (%s, %s)"
                cursor.execute(sql, (topic_id, words))

            # 提交更改
            connection.commit()
    finally:
        connection.close()


# 从数据库中获取评论数据
def fetch_comments_from_db():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT message FROM data_message"
            cursor.execute(sql)
            results = cursor.fetchall()
            comments = [result['message'] for result in results if result['message']]
            return comments
    finally:
        connection.close()

def filter_chinese_and_punctuation(text):
    # 使用正则表达式匹配中文和标点符号
    chinese_and_punctuation_pattern = re.compile(r'[\u4e00-\u9fff，。？！；：“”（）【】、]')
    # 过滤文本中的其他字符
    filtered_text = ''.join(chinese_and_punctuation_pattern.findall(text))
    return filtered_text


# 对评论进行主题建模
def lda_topic_modeling(comments, num_topics=15):
    # 分词
    texts = [comment.split() for comment in comments]

    # 创建词典
    dictionary = corpora.Dictionary(texts)

    # 创建语料库
    corpus = [dictionary.doc2bow(text) for text in texts]

    # 使用LDA模型拟合语料库
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

    return lda_model


# 主函数
def main():
    # 获取评论数据
    comments = fetch_comments_from_db()

    # 进行主题建模
    lda_model = lda_topic_modeling(comments)

    # 存储主题模型结果到数据库
    save_to_database(lda_model)

    # 打印主题
    for idx, topic in lda_model.print_topics(-1):
        topic=filter_chinese_and_punctuation(topic)
        print(f'Topic: {idx} \nWords: {topic}\n')


if __name__ == "__main__":
    main()
