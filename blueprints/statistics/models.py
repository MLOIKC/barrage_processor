from collections import Counter
from datetime import datetime
from collections import defaultdict
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app import db
from blueprints.danmu.models import get_latest_analysis_range


class KeywordsAnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    danmu_type = db.Column(db.String(255), nullable=False)
    danmu_data = db.Column(db.String(255), nullable=False)
    start_danmu_id = db.Column(db.String(255), nullable=False)
    end_danmu_id = db.Column(db.String(255), nullable=False)
    analysis_timestamp = db.Column(db.Integer)
    word_data = db.Column(db.JSON)


def get_keywords(danmu_type, danmu_data, processed_data):
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

    start_id, end_id = get_latest_analysis_range()
    save_keywords_analysis_result(danmu_type, danmu_data, start_id, end_id, word_data)
    return word_data


def save_keywords_analysis_result(danmu_type, danmu_data, start_id, end_id, word_data):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # Get current timestamp
        analysis_timestamp = int(datetime.now().timestamp())
        analysis = KeywordsAnalysisResult(
            danmu_type=danmu_type,
            danmu_data=danmu_data,
            start_danmu_id=start_id,
            end_danmu_id=end_id,
            analysis_timestamp=analysis_timestamp,
            word_data=word_data
        )
        db.session.add(analysis)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving keywords analysis result: {e}")
        db.session.rollback()
        return False


class TimeAnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    danmu_type = db.Column(db.String(255), nullable=False)
    danmu_data = db.Column(db.String(255), nullable=False)
    start_danmu_id = db.Column(db.String(255), nullable=False)
    end_danmu_id = db.Column(db.String(255), nullable=False)
    analysis_timestamp = db.Column(db.Integer)
    time_data = db.Column(db.JSON)


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

    start_id, end_id = get_latest_analysis_range()
    save_time_analysis_result(danmu_type, danmu_data, start_id, end_id, processed_data)
    return processed_data


def save_time_analysis_result(danmu_type, danmu_data, start_id, end_id, time_data):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # Get current timestamp
        analysis_timestamp = int(datetime.now().timestamp())
        analysis = TimeAnalysisResult(
            danmu_type=danmu_type,
            danmu_data=danmu_data,
            start_danmu_id=start_id,
            end_danmu_id=end_id,
            analysis_timestamp=analysis_timestamp,
            time_data=time_data
        )
        db.session.add(analysis)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving time analysis result: {e}")
        db.session.rollback()
        return False


class DateAnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    danmu_type = db.Column(db.String(255), nullable=False)
    danmu_data = db.Column(db.String(255), nullable=False)
    start_danmu_id = db.Column(db.String(255), nullable=False)
    end_danmu_id = db.Column(db.String(255), nullable=False)
    analysis_timestamp = db.Column(db.Integer)
    date_data = db.Column(db.JSON)


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

    start_id, end_id = get_latest_analysis_range()
    save_date_analysis_result(danmu_type, danmu_data, start_id, end_id, processed_data)
    return processed_data


def save_date_analysis_result(danmu_type, danmu_data, start_id, end_id, date_data):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # Get current timestamp
        analysis_timestamp = int(datetime.now().timestamp())
        analysis = DateAnalysisResult(
            danmu_type=danmu_type,
            danmu_data=danmu_data,
            start_danmu_id=start_id,
            end_danmu_id=end_id,
            analysis_timestamp=analysis_timestamp,
            date_data=date_data
        )
        db.session.add(analysis)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving date analysis result: {e}")
        db.session.rollback()
        return False


class ColorAnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    danmu_type = db.Column(db.String(255), nullable=False)
    danmu_data = db.Column(db.String(255), nullable=False)
    start_danmu_id = db.Column(db.String(255), nullable=False)
    end_danmu_id = db.Column(db.String(255), nullable=False)
    analysis_timestamp = db.Column(db.Integer)
    color_data = db.Column(db.JSON)


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

    start_id, end_id = get_latest_analysis_range()
    save_color_analysis_result(danmu_type, danmu_data, start_id, end_id, processed_data)
    return processed_data


def save_color_analysis_result(danmu_type, danmu_data, start_id, end_id, color_data):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # Get current timestamp
        analysis_timestamp = int(datetime.now().timestamp())
        analysis = ColorAnalysisResult(
            danmu_type=danmu_type,
            danmu_data=danmu_data,
            start_danmu_id=start_id,
            end_danmu_id=end_id,
            analysis_timestamp=analysis_timestamp,
            color_data=color_data
        )
        db.session.add(analysis)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving color analysis result: {e}")
        db.session.rollback()
        return False


class UserAnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    danmu_type = db.Column(db.String(255), nullable=False)
    danmu_data = db.Column(db.String(255), nullable=False)
    start_danmu_id = db.Column(db.String(255), nullable=False)
    end_danmu_id = db.Column(db.String(255), nullable=False)
    analysis_timestamp = db.Column(db.Integer)
    user_data = db.Column(db.JSON)


def process_database_userdata(danmu_type, danmu_data):
    DATABASE_URI = 'mysql://root:123456@localhost:3306/barrage'
    engine = create_engine(DATABASE_URI)

    # 创建数据库会话
    Session = sessionmaker(bind=engine)
    session = Session()

    # 根据不同的 danmu_type 构建不同的 SQL 查询语句
    if danmu_type != 'Adv':
        # 如果 danmu_type 不在预期的范围内，返回查询错误信息
        error_message = 'Invalid danmu_type'
        return {'error': error_message}

    query = session.query(text("midHash FROM rawdanmu_data WHERE bvid = :data")).params(data=danmu_data)
    user = query.all()

    query = session.query(text("ctime FROM rawdanmu_data WHERE bvid = :data")).params(data=danmu_data)
    timestamp = query.all()

    query = session.query(text("content FROM rawdanmu_data WHERE bvid = :data")).params(data=danmu_data)
    content = query.all()

    # 关闭数据库会话
    session.close()

    # 使用集合(Set)去重，得到发送弹幕的用户数量
    unique_users = set(user)
    num_users = len(unique_users)

    # 将字符串时间转换为日期时间对象，并提取小时数
    time_periods = []
    for ts_tuple in timestamp:
        ts_str = ts_tuple[0]  # 获取元组中的字符串时间
        dt = datetime.fromtimestamp(int(ts_str))  # 从时间戳字符串创建日期时间对象
        hour = dt.hour  # 获取小时数
        time_periods.append(hour)

    # 统计各时间段的数量
    period_counts = {}
    for period in time_periods:
        period_counts[period] = period_counts.get(period, 0) + 1

    # 提取统计结果作为折线图的数据，并按照小时从小到大排序
    sorted_counts = sorted(period_counts.items())
    hours = [hour for hour, count in sorted_counts]
    counts = [count for hour, count in sorted_counts]

    # 使用defaultdict创建一个字典，用于存储每个用户的弹幕数量和总长度
    user_stats = defaultdict(lambda: {'count': 0, 'total_length': 0})
    # 活跃用户数
    active_user = 0

    # 遍历user和content列表，统计每个用户的弹幕数量和总长度
    for u, c in zip(user, content):
        user_id = u[0]  # 获取用户标识
        user_stats[user_id]['count'] += 1  # 增加用户的弹幕数量
        user_stats[user_id]['total_length'] += len(c[0])  # 增加用户的弹幕总长度

    for user_id, stats in user_stats.items():
        if stats['count'] >= 5:
            active_user += 1

    # 统计所有用户的总弹幕数量和总长度
    total_count = sum(stats['count'] for stats in user_stats.values())
    total_length = sum(stats['total_length'] for stats in user_stats.values())

    # 计算所有用户的平均发布频率和长度
    total_avg_frequency = total_count / len(user_stats)
    total_avg_length = total_length / total_count

    processed_data = {
        'num_users': num_users,
        'hours': hours,
        'counts': counts,
        'total_avg_frequency': round(total_avg_frequency, 3),
        'total_avg_length': round(total_avg_length, 3),
        'active_user': active_user
    }
    start_id, end_id = get_latest_analysis_range()
    save_user_analysis_result(danmu_type, danmu_data, start_id, end_id, processed_data)
    return processed_data


def save_user_analysis_result(danmu_type, danmu_data, start_id, end_id, user_data):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # Get current timestamp
        analysis_timestamp = int(datetime.now().timestamp())
        analysis = UserAnalysisResult(
            danmu_type=danmu_type,
            danmu_data=danmu_data,
            start_danmu_id=start_id,
            end_danmu_id=end_id,
            analysis_timestamp=analysis_timestamp,
            user_data=user_data
        )
        db.session.add(analysis)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving color analysis result: {e}")
        db.session.rollback()
        return False
