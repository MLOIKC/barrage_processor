from flask import Blueprint, request, jsonify, make_response

from blueprints.sentiment.models import process_database_data
from blueprints.theme.models import lda_theme_analysis, lsa_theme_analysis, nmf_theme_analysis

theme_bp = Blueprint('theme', __name__)


@theme_bp.route('/analyze_theme', methods=['POST'])
def analyze_theme():
    try:
        # 获取前端发送的JSON数据
        request_data = request.json
        method = request_data.get('method')  # 获取前端传递的方法值
        # 从请求的 JSON 数据中获取 danmuDetail
        danmu_detail = request_data.get('danmuDetail')
        if danmu_detail:
            danmu_type = danmu_detail.get('type')
            danmu_data = danmu_detail.get('data')

            processed_data = process_database_data(danmu_type, danmu_data)

        # 根据不同的方法值进行主题分析处理
        if method == '1':
            result = lda_theme_analysis(danmu_type, danmu_data,processed_data)
        elif method == '2':
            result = lsa_theme_analysis(danmu_type, danmu_data,processed_data)
        elif method == '3':
            result = nmf_theme_analysis(danmu_type, danmu_data,processed_data)
        else:
            return jsonify({'error': 'Invalid method value'}), 400

        # 返回处理结果给前端
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
