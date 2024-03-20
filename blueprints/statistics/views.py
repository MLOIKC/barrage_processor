from flask import Blueprint, request, jsonify, make_response

from blueprints.sentiment.models import process_database_data
from blueprints.statistics.models import get_keywords

stat_bp = Blueprint('stat', __name__)


@stat_bp.route('/analyze_keywords', methods=['POST'])
def analyze_keywords():
    try:
        # 从请求的 JSON 数据中获取 danmuDetail
        danmu_detail = request.json.get('danmuDetail')
        if danmu_detail:
            danmu_type = danmu_detail.get('type')
            danmu_data = danmu_detail.get('data')

            processed_data = process_database_data(danmu_type, danmu_data)

            return jsonify(get_keywords(processed_data))
        else:
            return jsonify({'error': 'Invalid request data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

