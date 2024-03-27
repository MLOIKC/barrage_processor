from app import db


class DanmuData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    time = db.Column(db.String(255))
    content = db.Column(db.String(255))
    date = db.Column(db.String(255))

    __tablename__ = 'danmu_data'  # 指定表名


class DanmuDataHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    time = db.Column(db.String(255))
    content = db.Column(db.String(255))
    date = db.Column(db.String(255))

    __tablename__ = 'danmu_data_history'


class FullDanmuData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bvid = db.Column(db.String(255))
    content = db.Column(db.String(255))
    time = db.Column(db.Float)  # 假设时间是浮点数
    mode = db.Column(db.Integer)
    fontSize = db.Column(db.Integer)
    color = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    pool = db.Column(db.Integer)
    senderId = db.Column(db.String(255))
    rowId = db.Column(db.String(255))

    __tablename__ = 'fulldanmu_data'  # 指定表名


class FullDanmuDataHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bvid = db.Column(db.String(255))
    content = db.Column(db.String(255))
    time = db.Column(db.Float)  # 假设时间是浮点数
    mode = db.Column(db.Integer)
    fontSize = db.Column(db.Integer)
    color = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)
    pool = db.Column(db.Integer)
    senderId = db.Column(db.String(255))
    rowId = db.Column(db.String(255))

    __tablename__ = 'fulldanmu_data_history'


class RawDanmuData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bvid = db.Column(db.String(255))
    progress = db.Column(db.Integer)
    mode = db.Column(db.Integer)
    fontsize = db.Column(db.Integer)
    color = db.Column(db.Integer)
    midHash = db.Column(db.String(255))
    content = db.Column(db.String(255))
    ctime = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    idStr = db.Column(db.String(255))

    __tablename__ = 'rawdanmu_data'  # 指定表名


class RawDanmuDataHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bvid = db.Column(db.String(255))
    progress = db.Column(db.Integer)
    mode = db.Column(db.Integer)
    fontsize = db.Column(db.Integer)
    color = db.Column(db.Integer)
    midHash = db.Column(db.String(255))
    content = db.Column(db.String(255))
    ctime = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    idStr = db.Column(db.String(255))

    __tablename__ = 'rawdanmu_data_history'  # 指定表名


class DanmuAnalysisRange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_id = db.Column(db.Integer, nullable=False)
    end_id = db.Column(db.Integer, nullable=False)

    __tablename__ = 'danmu_analysis_range'


def save_danmu_to_database(danmu_title, danmu_times, danmu_contents, danmu_dates):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # 首先清空DanmuData表中的所有数据
        db.session.query(DanmuData).delete()
        # 获取当前数据库中最后一个弹幕的ID，并将起始ID设为这个值加1
        last_id = db.session.query(db.func.max(DanmuDataHistory.id)).scalar() or 0
        start_id = last_id + 1
        # 添加新数据到DanmuData和DanmuDataHistory
        for time, content, date in zip(danmu_times, danmu_contents, danmu_dates):
            danmu_data = DanmuData(title=danmu_title, time=time, content=content, date=date)
            danmu_data_history = DanmuDataHistory(title=danmu_title, time=time, content=content, date=date)
            db.session.add(danmu_data)
            db.session.add(danmu_data_history)
        db.session.commit()
        # 在数据提交后获取结束ID，此时它将反映最新的数据库状态
        end_id = db.session.query(db.func.max(DanmuDataHistory.id)).scalar() or 0
        # 首先清空DanmuAnalysisRange表中的所有数据
        db.session.query(DanmuAnalysisRange).delete()
        range_record = DanmuAnalysisRange(start_id=start_id, end_id=end_id)
        db.session.add(range_record)
        db.session.commit()
        return True
    except Exception as e:
        print("Error saving danmu to database:", str(e))
        db.session.rollback()
        return False


def save_fulldanmu_to_database(danmu_full_bvid, danmu_full_content, danmu_full_time, danmu_full_mode,
                               danmu_full_fontSize, danmu_full_color, danmu_full_timestamp, danmu_full_pool,
                               danmu_full_senderId, danmu_full_rowId):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # 首先清空FullDanmuData表中的所有数据
        db.session.query(FullDanmuData).delete()
        # 获取当前数据库中最后一个弹幕的ID，并将起始ID设为这个值加1
        last_id = db.session.query(db.func.max(FullDanmuDataHistory.id)).scalar() or 0
        start_id = last_id + 1
        # 添加新数据到FullDanmuData和FullDanmuDataHistory
        for content, time, mode, fontSize, color, timestamp, pool, senderId, rowId in zip(danmu_full_content,
                                                                                          danmu_full_time,
                                                                                          danmu_full_mode,
                                                                                          danmu_full_fontSize,
                                                                                          danmu_full_color,
                                                                                          danmu_full_timestamp,
                                                                                          danmu_full_pool,
                                                                                          danmu_full_senderId,
                                                                                          danmu_full_rowId):
            danmu_data = FullDanmuData(bvid=danmu_full_bvid, content=content, time=time, mode=mode, fontSize=fontSize,
                                       color=color,
                                       timestamp=timestamp, pool=pool, senderId=senderId, rowId=rowId)
            danmu_data_history = FullDanmuDataHistory(bvid=danmu_full_bvid, content=content, time=time, mode=mode,
                                                      fontSize=fontSize,
                                                      color=color,
                                                      timestamp=timestamp, pool=pool, senderId=senderId, rowId=rowId)
            db.session.add(danmu_data)
            db.session.add(danmu_data_history)

        db.session.commit()
        # 在数据提交后获取结束ID，此时它将反映最新的数据库状态
        end_id = db.session.query(db.func.max(FullDanmuDataHistory.id)).scalar() or 0
        # 首先清空DanmuAnalysisRange表中的所有数据
        db.session.query(DanmuAnalysisRange).delete()
        range_record = DanmuAnalysisRange(start_id=start_id, end_id=end_id)
        db.session.add(range_record)
        db.session.commit()
        return True
    except Exception as e:
        print("Error saving fulldanmu to database:", str(e))
        db.session.rollback()
        return False


def save_rawdanmu_to_database(data, bvid):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # 首先清空RawDanmuData表中的所有数据
        db.session.query(RawDanmuData).delete()
        # 获取当前数据库中最后一个弹幕的ID，并将起始ID设为这个值加1
        last_id = db.session.query(db.func.max(RawDanmuDataHistory.id)).scalar() or 0
        start_id = last_id + 1
        # 添加新数据到RawDanmuData和RawDanmuDataHistory
        for elem in data['elems']:
            danmu = RawDanmuData(
                bvid=bvid,
                progress=elem.get('progress', None),
                mode=elem.get('mode', None),
                fontsize=elem.get('fontsize', None),
                color=elem.get('color', None),
                midHash=elem.get('midHash', None),
                content=elem.get('content', None),
                ctime=elem.get('ctime', None),
                weight=elem.get('weight', None),
                idStr=elem.get('idStr', None)
            )
            danmu_history = RawDanmuDataHistory(
                bvid=bvid,
                progress=elem.get('progress', None),
                mode=elem.get('mode', None),
                fontsize=elem.get('fontsize', None),
                color=elem.get('color', None),
                midHash=elem.get('midHash', None),
                content=elem.get('content', None),
                ctime=elem.get('ctime', None),
                weight=elem.get('weight', None),
                idStr=elem.get('idStr', None)
            )
            db.session.add(danmu)
            db.session.add(danmu_history)

        db.session.commit()
        # 在数据提交后获取结束ID，此时它将反映最新的数据库状态
        end_id = db.session.query(db.func.max(RawDanmuDataHistory.id)).scalar() or 0
        # 首先清空DanmuAnalysisRange表中的所有数据
        db.session.query(DanmuAnalysisRange).delete()
        range_record = DanmuAnalysisRange(start_id=start_id, end_id=end_id)
        db.session.add(range_record)
        db.session.commit()
        return True
    except Exception as e:
        print("Error saving danmu to database:", str(e))
        db.session.rollback()
        return False


def get_latest_analysis_range():
    range_record = DanmuAnalysisRange.query.order_by(DanmuAnalysisRange.id.desc()).first()
    if range_record:
        return range_record.start_id, range_record.end_id
    else:
        return None, None
