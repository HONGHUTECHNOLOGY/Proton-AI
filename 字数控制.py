def truncate_to_5000(long_text):
    if len(long_text) <= 5000:
        return long_text
    
    # 找到5000字符位置前的最后一个空格
    truncated = long_text[:5000]
    last_space = truncated.rfind(' ')
    
    if last_space == -1:  # 如果没有找到空格，直接截断
        return truncated
    else:
        return truncated[:last_space]  # 保留最后一个完整单词
