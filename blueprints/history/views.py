from flask import Blueprint, request, jsonify, make_response

from blueprints.sentiment.models import SentimentAnalysisResult
from blueprints.statistics.models import KeywordsAnalysisResult, TimeAnalysisResult, DateAnalysisResult, \
    ColorAnalysisResult, UserAnalysisResult
from blueprints.theme.models import ThemeAnalysisResult

history_bp = Blueprint('history', __name__)


@history_bp.route('/get_sentiment_analysis_history', methods=['POST'])
def get_sentiment_analysis_history():
    # 从请求的 JSON 数据中获取 danmuDetail
    danmu_detail = request.json.get('danmuDetail')
    if danmu_detail:
        danmu_type = danmu_detail.get('type')
        # 查询数据库，过滤出符合条件的历史分析结果记录
        history_results = SentimentAnalysisResult.query.filter_by(danmu_type=danmu_type).all()
        # 提取需要的字段信息，如 danmu_data 和 analysis_timestamp
        history_data = [{'danmu_data': result.danmu_data, 'analysis_timestamp': result.analysis_timestamp,
                         'sentiment_data': result.sentiment_data} for result in history_results]
        # 返回组织好的数据作为响应
        return jsonify({'history_data': history_data})
    else:
        return jsonify({'error': 'Invalid request data'})


@history_bp.route('/get_theme_analysis_history', methods=['POST'])
def get_theme_analysis_history():
    # 从请求的 JSON 数据中获取 danmuDetail
    danmu_detail = request.json.get('danmuDetail')
    if danmu_detail:
        danmu_type = danmu_detail.get('type')
        # 查询数据库，过滤出符合条件的历史分析结果记录
        history_results = ThemeAnalysisResult.query.filter_by(danmu_type=danmu_type).all()
        # 提取需要的字段信息，如 danmu_data 和 analysis_timestamp
        history_data = [{'danmu_data': result.danmu_data, 'analysis_timestamp': result.analysis_timestamp,
                         'theme_method': result.theme_method, 'theme_words': result.theme_words} for result in
                        history_results]
        # 返回组织好的数据作为响应
        return jsonify({'history_data': history_data})
    else:
        return jsonify({'error': 'Invalid request data'})


@history_bp.route('/get_keywords_analysis_history', methods=['POST'])
def get_keywords_analysis_history():
    # 从请求的 JSON 数据中获取 danmuDetail
    danmu_detail = request.json.get('danmuDetail')
    if danmu_detail:
        danmu_type = danmu_detail.get('type')
        # 查询数据库，过滤出符合条件的历史分析结果记录
        history_results = KeywordsAnalysisResult.query.filter_by(danmu_type=danmu_type).all()
        # 提取需要的字段信息，如 danmu_data 和 analysis_timestamp
        history_data = [{'danmu_data': result.danmu_data, 'analysis_timestamp': result.analysis_timestamp,
                         'word_data': result.word_data} for result in history_results]
        # 返回组织好的数据作为响应
        return jsonify({'history_data': history_data})
    else:
        return jsonify({'error': 'Invalid request data'})


@history_bp.route('/get_time_analysis_history', methods=['POST'])
def get_time_analysis_history():
    # 从请求的 JSON 数据中获取 danmuDetail
    danmu_detail = request.json.get('danmuDetail')
    if danmu_detail:
        danmu_type = danmu_detail.get('type')
        # 查询数据库，过滤出符合条件的历史分析结果记录
        history_results = TimeAnalysisResult.query.filter_by(danmu_type=danmu_type).all()
        # 提取需要的字段信息，如 danmu_data 和 analysis_timestamp
        history_data = [{'danmu_data': result.danmu_data, 'analysis_timestamp': result.analysis_timestamp,
                         'time_data': result.time_data} for result in history_results]
        # 返回组织好的数据作为响应
        return jsonify({'history_data': history_data})
    else:
        return jsonify({'error': 'Invalid request data'})


@history_bp.route('/get_date_analysis_history', methods=['POST'])
def get_date_analysis_history():
    # 从请求的 JSON 数据中获取 danmuDetail
    danmu_detail = request.json.get('danmuDetail')
    if danmu_detail:
        danmu_type = danmu_detail.get('type')
        # 查询数据库，过滤出符合条件的历史分析结果记录
        history_results = DateAnalysisResult.query.filter_by(danmu_type=danmu_type).all()
        # 提取需要的字段信息，如 danmu_data 和 analysis_timestamp
        history_data = [{'danmu_data': result.danmu_data, 'analysis_timestamp': result.analysis_timestamp,
                         'date_data': result.date_data} for result in history_results]
        # 返回组织好的数据作为响应
        return jsonify({'history_data': history_data})
    else:
        return jsonify({'error': 'Invalid request data'})


@history_bp.route('/get_color_analysis_history', methods=['POST'])
def get_color_analysis_history():
    # 从请求的 JSON 数据中获取 danmuDetail
    danmu_detail = request.json.get('danmuDetail')
    if danmu_detail:
        danmu_type = danmu_detail.get('type')
        # 查询数据库，过滤出符合条件的历史分析结果记录
        history_results = ColorAnalysisResult.query.filter_by(danmu_type=danmu_type).all()
        # 提取需要的字段信息，如 danmu_data 和 analysis_timestamp
        history_data = [{'danmu_data': result.danmu_data, 'analysis_timestamp': result.analysis_timestamp,
                         'color_data': result.color_data} for result in history_results]
        # 返回组织好的数据作为响应
        return jsonify({'history_data': history_data})
    else:
        return jsonify({'error': 'Invalid request data'})


@history_bp.route('/get_user_analysis_history', methods=['POST'])
def get_user_analysis_history():
    # 从请求的 JSON 数据中获取 danmuDetail
    danmu_detail = request.json.get('danmuDetail')
    if danmu_detail:
        danmu_type = danmu_detail.get('type')
        # 查询数据库，过滤出符合条件的历史分析结果记录
        history_results = UserAnalysisResult.query.filter_by(danmu_type=danmu_type).all()
        # 提取需要的字段信息，如 danmu_data 和 analysis_timestamp
        history_data = [{'danmu_data': result.danmu_data, 'analysis_timestamp': result.analysis_timestamp,
                         'user_data': result.user_data} for result in history_results]
        # 返回组织好的数据作为响应
        return jsonify({'history_data': history_data})
    else:
        return jsonify({'error': 'Invalid request data'})
