from gensim import corpora, models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, NMF


def lda_theme_analysis(processed_data):
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

    # 将提取的主题词返回给前端
    return topics


def lsa_theme_analysis(processed_data):
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

    return topic_key_terms


def nmf_theme_analysis(processed_data):
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

    return topic_key_terms
