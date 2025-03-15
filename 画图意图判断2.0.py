import re

def detect_draw_intent(text):
    # 排除的无关场景（如“画画是爱好”）
    exclude_pattern = re.compile(
        r'(画画|绘图|作图)(是|的|一种|作为)|^.*?(聊天|说话|文本|回答)',
        re.IGNORECASE
    )
    
    # 否定词检测（如“不要画”）
    negate_pattern = re.compile(
        r'(不|不要|别|无需|不能|不需要|不想|莫|勿)\s*.*?(画|绘制|生成|创建)(图|图像|图片)?',
        re.IGNORECASE
    )
    
    # 绘画意图匹配（不再要求量词，如“一张”）
    paint_pattern = re.compile(
        r'(?:请|帮我|想要|需要|能否)?\s*'  # 可选请求词
        r'(画|绘制|生成|创建|设计)\s*'    # 核心动词
        r'(?:的|一个|一张)?\s*'           # 可选修饰词（非必须）
        r'(图|图像|图片|照片|海报|插图|设计|概念图)|'  # 图像类名词
        r'(画|绘制|生成|创建)\s*.*?\S+',  # 动词后直接跟对象（如“画猫”）
        re.IGNORECASE
    )
    
    # 先检查排除场景
    if exclude_pattern.search(text):
        return False
    
    # 检查否定词
    if negate_pattern.search(text):
        return False
    
    # 匹配绘画意图
    return bool(paint_pattern.search(text))