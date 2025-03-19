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
    
    # 绘画意图匹配（支持“给我”+图像名词的请求）
    paint_pattern = re.compile(
        r'(?:请|帮我|给我|想要|需要|能否)?\s*'  # 新增“给我”作为请求词
        r'(画|绘制|生成|创建|设计|给)\s*'      # 动词包含“给”，但需结合上下文
        r'(?:的|一个|一张)?\s*'
        r'(图|图像|图片|照片|海报|插图|设计|概念图)|'  # 图像类名词
        r'(画|绘制|生成|创建|给)\s*.*?\S+',    # 允许“给”后直接跟对象（需含图像关键词）
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
