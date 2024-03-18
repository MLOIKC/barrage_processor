from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from zhconv import convert
import jieba
import re
import os

# 获取停用词文件路径为当前文件夹中的 stoplist_new.txt
current_directory = os.getcwd()
stopword_file_path = os.path.join(current_directory, 'blueprints\\sentiment\\stoplist_new.txt')
# 读取程度词和否定词
degreeword_file_path = os.path.join(current_directory, 'blueprints\\sentiment\\degree_new.txt')
negationword_file_path = os.path.join(current_directory, 'blueprints\\sentiment\\notlist_new.txt')
# 读取情感词典
sentiment_dict_path = os.path.join(current_directory, 'blueprints\\sentiment\\emotion.csv')


def process_database_data():
    DATABASE_URI = 'mysql://root:123456@localhost:3306/barrage'
    engine = create_engine(DATABASE_URI)

    # 创建数据库会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 使用 text() 函数将 SQL 语句转换为文本表达式
    query = session.query(text("content FROM rawdanmu_data"))
    contents = query.all()

    # 关闭数据库会话
    session.close()
    # 读取停用词文件
    stopwords = set()
    with open(stopword_file_path, 'r', encoding='utf-8') as stopword_file:
        stopwords.update(word.strip() for word in stopword_file.readlines())

    processed_data = []
    for content in contents:
        traditional_chinese = content[0]  # 因为查询返回的是元组，content 是第一个元素
        simplified_chinese = convert(traditional_chinese, 'zh-hans')
        filtered_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', simplified_chinese)  # 过滤非中文字符、数字和字母
        segmented_content = ' '.join(filter(lambda x: x not in stopwords, jieba.cut(filtered_text)))  # 使用过滤后的文本进行中文分词

        processed_data.append({
            'original_content': traditional_chinese,
            'simplified_content': simplified_chinese,
            'filtered_content': filtered_text,
            'segmented_content': segmented_content
        })

    return processed_data


def load_word_dict(file_path):
    word_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word, value = parts[0], float(parts[1])
                word_dict[word] = value
    return word_dict


def get_major_emotion_category(emotion_code):
    # 根据情感代号获取大类
    major_categories = {
        'PA': 'Joy',
        'PE': 'Joy',
        'PD': 'Good',
        'PH': 'Good',
        'PG': 'Good',
        'PB': 'Good',
        'PK': 'Good',
        'NA': 'Anger',
        'NB': 'Sadness',
        'NJ': 'Sadness',
        'NH': 'Sadness',
        'PF': 'Sadness',
        'NI': 'Fear',
        'NC': 'Fear',
        'NG': 'Fear',
        'NE': 'Disgust',
        'ND': 'Disgust',
        'NN': 'Disgust',
        'NK': 'Disgust',
        'NL': 'Disgust',
        'PC': 'Surprise',
    }
    return major_categories.get(emotion_code, 'Unknown')


def load_sentiment_dict(sentiment_dict_path):
    sentiment_dict = {}
    with open(sentiment_dict_path, 'r', encoding='utf-8') as f:
        # 跳过表头
        next(f)
        for line in f:
            parts = line.strip().split(',')
            word = parts[0]
            emotion = parts[4]
            try:
                intensity = float(parts[5])
            except ValueError:
                intensity = 5
            if word not in sentiment_dict or intensity > sentiment_dict[word][1]:
                sentiment_dict[word] = (emotion, intensity)
    return sentiment_dict


def match_and_save(processed_data):
    degree_words = load_word_dict(degreeword_file_path)
    negation_words = load_word_dict(negationword_file_path)
    sentiment_dict = load_sentiment_dict(sentiment_dict_path)
    count_non_empty_emotion = 0  # 记录情感类别不为空的词的数量
    count_emotion = 0  # 记录词的数量
    major_categories_count = {'Joy': 0, 'Good': 0, 'Anger': 0,
                              'Sadness': 0, 'Fear': 0, 'Disgust': 0, 'Surprise': 0, 'Unknown': 0}
    overall_categories_count = {'Positive': 0, 'Negative': 0, 'Unknown': 0}

    for line in processed_data:
        # 直接按空格划分单词
        words = line['segmented_content'].strip().split()

        total_intensity = 0

        for word in words:
            if word in sentiment_dict:
                # 如果词语在情感词典中
                emotion, intensity = sentiment_dict[word]
                if emotion:
                    if emotion in ('PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK', 'PC'):
                        total_intensity += intensity
                    else:
                        total_intensity -= intensity
            else:
                # 如果词语不在情感词典中，检查是否包含程度词或否定词
                adjusted_intensity = 0  # 初始化一个调整后的情感强度，默认为零
                found_modifier = False  # 用于标记是否找到了程度词或否定词，默认为 False

                # 第一个循环：处理程度词
                for modifier, value in degree_words.items():
                    if modifier in word:  # 如果词语中包含程度词
                        # 如果程度词本身就是一个词语，考虑其后面一个词语的情感强度
                        if modifier == word:
                            next_word_index = words.index(word) + 1
                            if next_word_index < len(words):
                                next_word = words[next_word_index]
                                emotion, next_word_intensity = sentiment_dict.get(next_word, ('', 0))
                                # 根据情感词的正负判断取正值还是负值
                                next_word_intensity *= 1 if emotion and emotion in (
                                'PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK', 'PC') else -1
                                adjusted_intensity += next_word_intensity * value
                                # print(f"程度词划分1：{modifier}/{word}/{next_word}/{next_word_intensity}/{value}")
                                found_modifier = True  # 标记找到了程度词
                                break
                        # 如果程度词位于词语首部
                        elif word.startswith(modifier):
                            part = word.replace(modifier, "", 1)  # 从词语中去除程度词
                            emotion, base_intensity = sentiment_dict.get(part, ('', 0))  # 获取去除程度词后词的情感类别和强度
                            # 根据情感词的正负判断取正值还是负值
                            base_intensity *= 1 if emotion and emotion in (
                            'PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK', 'PC') else -1
                            adjusted_intensity += base_intensity * value  # 用程度词的强度值乘以去除程度词后词的情感强度
                            adjusted_intensity -= base_intensity  # 若程度词后词在第一个判断中已经计算过了故需要减去
                            # print(f"程度词划分2：{modifier}/{word}/{base_intensity}/{value}")
                            found_modifier = True  # 标记找到了程度词
                            break

                # 第二个循环：处理否定词
                for modifier, value in negation_words.items():
                    if modifier in word:  # 如果词语中包含否定词
                        # 如果否定词本身就是一个词语，考虑其后面一个词语的情感强度
                        if modifier == word:
                            next_word_index = words.index(word) + 1
                            if next_word_index < len(words):
                                next_word = words[next_word_index]
                                emotion, next_word_intensity = sentiment_dict.get(next_word, ('', 0))
                                # 根据情感词的正负判断取正值还是负值
                                next_word_intensity *= 1 if emotion and emotion in (
                                'PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK', 'PC') else -1
                                adjusted_intensity -= next_word_intensity * value
                                # print(f"否定词划分1：{modifier}/{word}/{next_word}/{next_word_intensity}/{value}")
                                found_modifier = True  # 标记找到了否定词
                                break
                        # 如果否定词位于词语首部
                        elif word.startswith(modifier):
                            part = word.replace(modifier, "", 1)  # 从词语中去除否定词
                            emotion, base_intensity = sentiment_dict.get(part, ('', 0))  # 获取去除否定词后词的情感类别和强度
                            # 根据情感词的正负判断取正值还是负值
                            base_intensity *= 1 if emotion and emotion in (
                            'PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK', 'PC') else -1
                            adjusted_intensity -= base_intensity * value  # 用否定词的强度值乘以去除否定词后词的情感强度
                            adjusted_intensity -= base_intensity  # 若否定词后词在第一个判断中已经计算过了故需要减去
                            # print(f"否定词划分2：{modifier}/{word}/{base_intensity}/{value}")
                            found_modifier = True  # 标记找到了否定词
                            break

                # 如果找到了程度词或否定词并成功调整了强度
                if found_modifier:
                    total_intensity += adjusted_intensity
                # 否则，不调整强度

        # 匹配情感词典
        emotions = [sentiment_dict.get(word, ('', 0)) for word in words]

        # 判断情感类别是否为空
        if any(emotion[0] != '' for emotion in emotions):
            count_non_empty_emotion += 1

        count_emotion += 1

        # 判断总体情感是积极还是消极
        if total_intensity > 0:
            overall_category = 'Positive'
        elif total_intensity < 0:
            overall_category = 'Negative'
        else:
            overall_category = 'Unknown'

        overall_categories_count[overall_category] += 1

        # 获取最大强度的情感类别
        max_emotion = max(emotions, key=lambda x: x[1], default=('', 0))
        major_category = get_major_emotion_category(max_emotion[0])

        major_categories_count[major_category] += 1

        line['major_emotion'] = major_category
        line['overall_emotion'] = overall_category

    # print(f"情感类别不为空的词的数量: {count_non_empty_emotion}/{count_emotion}")
    # print("情感大类统计:")
    # for category, count in major_categories_count.items():
    #     print(f"{category}: {count}")
    #
    # print("整体情感大类统计:")
    # for category, count in overall_categories_count.items():
    #     print(f"{category}: {count}")
