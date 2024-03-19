from flask import Blueprint, request, jsonify, make_response
from google.protobuf.json_format import MessageToJson, MessageToDict
from blueprints.danmu.danmu_pb2 import DmSegMobileReply
import os
from . import models

# 创建蓝图对象
danmu_bp = Blueprint('danmu', __name__)

# 获取当前脚本所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 构建文件路径
file_path = os.path.join(current_directory, "seg.so")

@danmu_bp.route('/receive-danmu', methods=['POST'])
def receive_danmu():
    try:
        data = request.get_json()
        danmu_title = data.get('titledata', 'No Title')
        danmu_times = data.get('timedata', [])
        danmu_contents = data.get('contentdata', [])
        danmu_dates = data.get('datedata', [])

        saved = models.save_danmu_to_database(danmu_title, danmu_times, danmu_contents, danmu_dates)
        if saved:
            # 返回成功响应
            response_data = {"message": "数据接收并成功保存"}
            return make_response(jsonify(response_data), 200)
        else:
            # 返回错误响应
            response_data = {"error": "数据获取与保存失败"}
            return make_response(jsonify(response_data), 500)

    except Exception as e:
        print("Error processing data:", str(e))

        # 返回错误响应
        response_data = {"error": "数据接收失败"}
        return make_response(jsonify(response_data), 500)


@danmu_bp.route('/receive-fulldanmu', methods=['POST'])
def receive_fulldanmu():
    try:
        data = request.get_json()
        danmu_full_bvid = data.get('bvid', 'No Bvid')
        danmu_full_content = data.get('contents', [])
        danmu_full_time = data.get('times', [])
        danmu_full_mode = data.get('modes', [])
        danmu_full_fontSize = data.get('fontSizes', [])
        danmu_full_color = data.get('colors', [])
        danmu_full_timestamp = data.get('timestamps', [])
        danmu_full_pool = data.get('pools', [])
        danmu_full_senderId = data.get('senderIds', [])
        danmu_full_rowId = data.get('rowIds', [])

        saved = models.save_fulldanmu_to_database(danmu_full_bvid, danmu_full_content, danmu_full_time, danmu_full_mode,
                                                  danmu_full_fontSize, danmu_full_color, danmu_full_timestamp,
                                                  danmu_full_pool,
                                                  danmu_full_senderId, danmu_full_rowId)

        if saved:
            # 返回成功响应
            response_data = {"message": "数据接收并成功保存"}
            return make_response(jsonify(response_data), 200)
        else:
            # 返回错误响应
            response_data = {"error": "数据保存失败"}
            return make_response(jsonify(response_data), 500)

    except Exception as e:
        print("Error processing data:", str(e))

        # 返回错误响应
        response_data = {"error": "数据接收失败"}
        return make_response(jsonify(response_data), 500)

@danmu_bp.route('/receive-rawdanmu', methods=['POST'])
def receive_rawdanmu():
    try:
        bvid = request.form.get('bvid')
        # 从请求的 body 中获取原始二进制数据
        protobuf_data = request.files['protobufData'].read()

        # 使用 Protobuf 解析数据
        dm_reply = DmSegMobileReply()
        dm_reply.ParseFromString(protobuf_data)

        # 将数据转换为字典
        data = MessageToDict(dm_reply)

        # 保存数据到数据库
        saved = models.save_rawdanmu_to_database(data, bvid)

        if saved:
            # 返回成功响应
            response_data = {"message": "数据接收并成功保存"}
            return make_response(jsonify(response_data), 200)
        else:
            # 返回错误响应
            response_data = {"error": "数据保存失败"}
            return make_response(jsonify(response_data), 500)

    except Exception as e:
        print("Error processing data:", str(e))

        # 返回错误响应
        response_data = {"error": "数据接收失败"}
        return make_response(jsonify(response_data), 500)
