from app import db


class DanmuData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    time = db.Column(db.String(255))
    content = db.Column(db.String(255))
    date = db.Column(db.String(255))

    __tablename__ = 'danmu_data'  # 指定表名


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


def save_danmu_to_database(danmu_title, danmu_times, danmu_contents, danmu_dates):
    try:
        db.create_all()
        for time, content, date in zip(danmu_times, danmu_contents, danmu_dates):
            danmu_data = DanmuData(title=danmu_title, time=time, content=content, date=date)
            db.session.add(danmu_data)
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
        db.create_all()
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
            db.session.add(danmu_data)

        db.session.commit()
        return True
    except Exception as e:
        print("Error saving fulldanmu to database:", str(e))
        db.session.rollback()
        return False


def save_rawdanmu_to_database(data, bvid):
    try:
        db.create_all()
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
            db.session.add(danmu)

        db.session.commit()
        return True
    except Exception as e:
        print("Error saving danmu to database:", str(e))
        db.session.rollback()
        return False
