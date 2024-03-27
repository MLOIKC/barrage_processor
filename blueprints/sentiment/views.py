from flask import Blueprint, request, jsonify, make_response

# 创建蓝图对象
from blueprints.sentiment.models import process_database_data, match_and_save

senti_bp = Blueprint('senti', __name__)


@senti_bp.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    # 从请求的 JSON 数据中获取 danmuDetail
    danmu_detail = request.json.get('danmuDetail')
    if danmu_detail:
        danmu_type = danmu_detail.get('type')
        danmu_data = danmu_detail.get('data')

        processed_data = process_database_data(danmu_type, danmu_data)
        result_data = match_and_save(danmu_type, danmu_data, processed_data)
    return jsonify({'sentiment': result_data})
