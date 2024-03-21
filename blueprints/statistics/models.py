from collections import Counter
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def get_keywords(processed_data):
    words_list = []
    for line in processed_data:
        # 按空格划分单词并筛选出长度大于1的词语
        words = [word for word in line['segmented_content'].strip().split() if len(word) > 1]
        words_list.append(words)
    # 将二维列表展平为一维列表
    flat_word_list = [word for sublist in words_list for word in sublist]

    # 使用 Counter 进行词频统计
    word_freq = Counter(flat_word_list)

    # 按照词频降序排列
    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # 只保留前100个词频数据
    top_word_freq = sorted_word_freq[:100]

    # 转换为前端需要的格式
    word_data = [{'text': word, 'frequency': freq} for word, freq in top_word_freq]

    return word_data


def process_database_timedata(danmu_type, danmu_data):
    DATABASE_URI = 'mysql://root:123456@localhost:3306/barrage'
    engine = create_engine(DATABASE_URI)

    # 创建数据库会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 根据不同的 danmu_type 构建不同的 SQL 查询语句
    if danmu_type == 'Beg':
        query = session.query(text("time FROM danmu_data WHERE title = :data")).params(data=danmu_data)
    elif danmu_type == 'Int':
        query = session.query(text("time FROM fulldanmu_data WHERE bvid = :data")).params(data=danmu_data)
    elif danmu_type == 'Adv':
        query = session.query(text("progress FROM rawdanmu_data WHERE bvid = :data")).params(data=danmu_data)
    else:
        # 如果 danmu_type 不在预期的范围内，返回查询错误信息
        error_message = 'Invalid danmu_type'
        return {'error': error_message}

    # 执行查询并获取结果
    contents = query.all()

    # 关闭数据库会话
    session.close()

    processed_data = []
    for content in contents:
        if danmu_type == 'Beg':
            # 分割时间字符串
            minutes, seconds = content[0].split(":")
            # 将小时和分钟转换为整数
            minutes = int(minutes)
            seconds = int(seconds)

            # 计算总的分钟数和对应的秒数
            time_data = minutes * 60 + seconds
        elif danmu_type == 'Int':
            time_data = content[0]
        elif danmu_type == 'Adv':
            if isinstance(content[0], (int, float)):
                time_data = content[0] / 1000

        processed_data.append({
            'time': time_data
        })

    return processed_data


def process_database_datedata(danmu_type, danmu_data):
    DATABASE_URI = 'mysql://root:123456@localhost:3306/barrage'
    engine = create_engine(DATABASE_URI)

    # 创建数据库会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 根据不同的 danmu_type 构建不同的 SQL 查询语句
    if danmu_type == 'Beg':
        query = session.query(text("date FROM danmu_data WHERE title = :data")).params(data=danmu_data)
    elif danmu_type == 'Int':
        query = session.query(text("timestamp FROM fulldanmu_data WHERE bvid = :data")).params(data=danmu_data)
    elif danmu_type == 'Adv':
        query = session.query(text("ctime FROM rawdanmu_data WHERE bvid = :data")).params(data=danmu_data)
    else:
        # 如果 danmu_type 不在预期的范围内，返回查询错误信息
        error_message = 'Invalid danmu_type'
        return {'error': error_message}

    # 执行查询并获取结果
    contents = query.all()

    # 关闭数据库会话
    session.close()

    processed_data = []
    for content in contents:
        if danmu_type == 'Adv':
            date_data = content[0] + '000'
        elif danmu_type == 'Int':
            date_data = content[0] * 1000
        else:
            date_data = content[0]  # 因为查询返回的是元组，content 是第一个元素

        processed_data.append({
            'date': date_data
        })

    return processed_data


# 转换颜色值为RGB
def convert_color_to_rgb(color):
    r = (color >> 16) & 255
    g = (color >> 8) & 255
    b = color & 255
    return r, g, b


def process_database_colordata(danmu_type, danmu_data):
    DATABASE_URI = 'mysql://root:123456@localhost:3306/barrage'
    engine = create_engine(DATABASE_URI)

    # 创建数据库会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 根据不同的 danmu_type 构建不同的 SQL 查询语句
    if danmu_type == 'Int':
        query = session.query(text("color FROM fulldanmu_data WHERE bvid = :data")).params(data=danmu_data)
    elif danmu_type == 'Adv':
        query = session.query(text("color FROM rawdanmu_data WHERE bvid = :data")).params(data=danmu_data)
    else:
        # 如果 danmu_type 不在预期的范围内，返回查询错误信息
        error_message = 'Invalid danmu_type'
        return {'error': error_message}

    # 执行查询并获取结果
    contents = query.all()

    # 关闭数据库会话
    session.close()

    processed_data = []
    for content in contents:
        processed_data.append({
            'color': convert_color_to_rgb(content[0])
        })

    return processed_data
