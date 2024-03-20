from collections import Counter


def get_keywords(processed_data):
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

    return word_data
