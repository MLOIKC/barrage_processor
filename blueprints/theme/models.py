from datetime import datetime

from gensim import corpora, models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, NMF
from app import db
from blueprints.danmu.models import get_latest_analysis_range


def lda_theme_analysis(danmu_type, danmu_data, processed_data):
    words_list = []
    for line in processed_data:
        # 按空格划分单词并筛选出长度大于1的词语
        words = [word for word in line['segmented_content'].strip().split() if len(word) > 1]
        words_list.append(words)

    # 创建词典（Dictionary）和文档词袋（Corpus）
    dictionary = corpora.Dictionary(words_list)
    corpus = [dictionary.doc2bow(words) for words in words_list]

    # 运行 LDA 模型
    lda_model = models.LdaMulticore(corpus, num_topics=5, id2word=dictionary, passes=5)
    # 提取五组主题词
    topics = []
    for topic_id in range(lda_model.num_topics):
        topic_words = [word.split('*')[1].strip().strip('"') for word in
                       lda_model.print_topic(topic_id, topn=5).split('+')]
        topics.append(topic_words)

    start_id, end_id = get_latest_analysis_range()
    theme_method = "lda"
    save_theme_analysis_result(danmu_type, danmu_data, start_id, end_id, theme_method, topics)
    # 将提取的主题词返回给前端
    return topics


def lsa_theme_analysis(danmu_type, danmu_data, processed_data):
    documents = []
    for line in processed_data:
        documents.append(line['segmented_content'])
    # 使用 TF-IDF 进行文本特征提取
    vectorizer = TfidfVectorizer(max_df=0.85, max_features=10000, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 使用 Truncated SVD 进行降维
    num_topics = 5  # 设置主题数
    lsa_model = TruncatedSVD(n_components=num_topics)
    lsa_topic_matrix = lsa_model.fit_transform(tfidf_matrix)

    # 输出主题词
    terms = vectorizer.get_feature_names_out()
    topic_key_terms = []
    for i, topic in enumerate(lsa_model.components_):
        topic_terms = [terms[index] for index in topic.argsort()[:-6:-1]]
        topic_key_terms.append(topic_terms)

    start_id, end_id = get_latest_analysis_range()
    theme_method = "lsa"
    save_theme_analysis_result(danmu_type, danmu_data, start_id, end_id, theme_method, topic_key_terms)
    return topic_key_terms


def nmf_theme_analysis(danmu_type, danmu_data, processed_data):
    documents = []
    for line in processed_data:
        documents.append(line['segmented_content'])
    # 使用 TF-IDF 进行文本特征提取
    vectorizer = TfidfVectorizer(max_df=0.85, max_features=10000, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 使用 Truncated SVD 进行降维
    num_topics = 5  # 设置主题数
    nmf_model = NMF(n_components=num_topics)
    nmf_topic_matrix = nmf_model.fit_transform(tfidf_matrix)

    # 输出主题词
    terms = vectorizer.get_feature_names_out()
    topic_key_terms = []
    for i, topic in enumerate(nmf_model.components_):
        topic_terms = [terms[index] for index in topic.argsort()[:-6:-1]]
        topic_key_terms.append(topic_terms)

    start_id, end_id = get_latest_analysis_range()
    theme_method = "nmf"
    save_theme_analysis_result(danmu_type, danmu_data, start_id, end_id, theme_method, topic_key_terms)
    return topic_key_terms


class ThemeAnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    danmu_type = db.Column(db.String(255), nullable=False)
    danmu_data = db.Column(db.String(255), nullable=False)
    start_danmu_id = db.Column(db.String(255), nullable=False)
    end_danmu_id = db.Column(db.String(255), nullable=False)
    analysis_timestamp = db.Column(db.Integer)
    theme_method = db.Column(db.String(255), nullable=False)
    theme_words = db.Column(db.JSON)  # 使用 JSON 类型存储主题词列表


def save_theme_analysis_result(danmu_type, danmu_data, start_id, end_id, theme_method, theme_words):
    try:
        # 创建所有表，如果尚未存在
        db.create_all()
        # Get current timestamp
        analysis_timestamp = int(datetime.now().timestamp())
        analysis = ThemeAnalysisResult(
            danmu_type=danmu_type,
            danmu_data=danmu_data,
            start_danmu_id=start_id,
            end_danmu_id=end_id,
            analysis_timestamp=analysis_timestamp,
            theme_method=theme_method,
            theme_words=theme_words
        )
        db.session.add(analysis)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error saving theme analysis result: {e}")
        db.session.rollback()
        return False
