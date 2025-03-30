import re
from typing import Tuple, Optional


def drawing_intention_judgement(text):
    def gemini(text):
        text = text.lower()

        # 优先检查是否包含明显的否定词，表示不是画图请求
        negative_patterns = [r"我画了", r"我想看", r"帮我找", r"哪里有", r"有没有", r"这不是", r"那不是"]
        for pattern in negative_patterns:
            if re.search(pattern, text):
                return False

        # 检查强烈的画图意图模式
        strong_patterns = [r"(请|帮我|我要|我想|需要|要求|来|做)一张?(个|幅)?(图|图片|图像|画作)",
                           r"(画|绘制|生成|创造).*?(图|图片|图像|画作)", r"(图|图片|图像|画作).*?(画|绘制|生成|创造)",
                           r"(画|绘制|生成).*?(风格|类型)", r"风格.*?的.*?图", r"类型.*?的.*?图", r"画.*?的",
                           r"绘制.*?的", r"生成.*?的", r"创造.*?的", r"来一张.*?的"]
        for pattern in strong_patterns:
            if re.search(pattern, text):
                return True

        # 检查画图相关的关键词
        keywords_draw = ["画", "绘制", "生成", "创造", "做", "来"]
        keywords_image = ["图", "图片", "图像", "画作"]
        auxiliary_request = ["一张", "一个", "一幅", "请", "想要", "需要", "要求", "帮我", "可以"]
        style_keywords = ["风格", "类型", "动漫", "油画", "水彩", "像素", "3d", "写实", "卡通", "抽象", "印象派",
                          "现代", "复古", "赛博朋克"]  # 更多风格词

        found_draw = any(keyword in text for keyword in keywords_draw)
        found_image = any(keyword in text for keyword in keywords_image)
        found_aux = any(keyword in text for keyword in auxiliary_request)
        found_style = any(keyword in text for keyword in style_keywords)

        # 结合关键词判断
        if found_draw and found_image and found_aux:
            return True

        # 处理疑问句，例如“你能不能画一张图？”
        if found_draw and found_image and any(keyword in text for keyword in ["吗", "呢", "么", "?"]) and any(
                keyword in text for keyword in ["可以", "能否", "会不会"]):
            return True

        # 处理“画出”的请求
        if "画出" in text and any(keyword in text for keyword in keywords_image):
            return True

        # 包含风格描述的画图请求
        if found_draw and found_style and found_image:
            return True

        # 更宽松的匹配，例如 "一张猫的图"
        if "一张" in text and any(keyword in text for keyword in keywords_image) and any(
                keyword in text for keyword in ["的"]):
            return True

        # 包含具体作画工具或平台的词汇 (可以根据实际情况添加)
        platform_keywords = ["midjourney", "stable diffusion", "dall-e", "mj", "sd"]
        if found_draw and any(keyword in text for keyword in platform_keywords):
            return True

        return False

    def claude(text):
        # 转换为小写以便不区分大小写
        text = text.lower()

        # 关键词列表：与绘图相关的动词
        drawing_verbs = ["画", "绘制", "绘画", "描绘", "创作", "制作", "生成", "做", "创建", "设计", "渲染", "构思",
                         "展示", "呈现"]

        # 关键词列表：与绘图相关的名词
        drawing_nouns = ["图", "画", "图片", "图像", "插图", "绘图", "素描", "插画", "漫画", "照片", "海报", "壁纸",
                         "logo", "标志", "封面", "画作", "艺术", "设计图", "创意图", "示意图", "概念图"]

        # 特定图像类型
        image_types = ["肖像", "风景", "动物", "卡通", "写实", "抽象", "二次元", "动漫", "风格", "水彩", "油画", "手绘",
                       "像素", "梦幻", "科幻", "现代", "复古", "中国风", "西方", "东方"]

        # 特定指令和提示词
        specific_instructions = ["帮我", "请", "能否", "能否帮我", "可以", "可否", "麻烦", "想要", "需要", "我想",
                                 "我需要", "我要"]

        # 否定词列表，这些词的存在可能表明用户实际上不是在请求绘图
        negative_indicators = ["不要画", "不想要图", "不需要图", "不用画", "别画", "无需绘制", "不必画", "不用绘制"]

        # 检查否定指示符
        for neg in negative_indicators:
            if neg in text:
                return False

        # 计算分数来判断是否是绘图请求
        score = 0

        # 检查是否包含绘图相关的动词
        for verb in drawing_verbs:
            if verb in text:
                score += 2
                break  # 只计算一次

        # 检查是否包含图像相关的名词
        for noun in drawing_nouns:
            if noun in text:
                score += 2
                break  # 只计算一次

        # 检查是否包含特定的图像类型
        for img_type in image_types:
            if img_type in text:
                score += 1
                break  # 只计算一次

        # 检查是否包含特定的指令或提示词
        for instr in specific_instructions:
            if instr in text:
                score += 1
                break  # 只计算一次

        # 匹配常见的绘图请求模式
        common_patterns = ["给我画", "帮我画", "能画", "可以画", "请画", "画一个", "画一张", "生成图片", "生成一张",
                           "做个图", "做一张图", "制作图片", "创建图像", "设计一个", "能否绘制", "请绘制", "绘制一张",
                           "渲染一个"]

        for pattern in common_patterns:
            if pattern in text:
                score += 3
                break  # 只计算一次

        # 检查是否有详细的图像描述（通常绘图请求会有详细描述）
        description_indicators = ["风格", "背景", "颜色", "色调", "姿势", "表情", "场景", "细节"]
        for indicator in description_indicators:
            if indicator in text:
                score += 1

        # 检查文本长度，详细的绘图请求通常较长
        if len(text) > 20:
            score += 1

        # 根据分数判断是否是绘图请求
        # 至少需要包含一个绘图动词和一个图像名词，或匹配一个常见模式
        return score >= 5

    def chatgpt(text):
        if not text:
            return False

        # 可能的画图关键词
        keywords = ["画", "绘制", "生成", "制作", "创作", "设计", "帮我画", "能画", "会画", "帮我生成", "能生成",
                    "画一个", "画出", "画张", "画幅", "绘个", "生成一张", "做一张", "做个图", "来张图", "整张图"]

        # 正则匹配一些可能的表述
        patterns = [r"(帮我|能|会)?(画|绘制|生成|做|设计)[一张个幅]?(.*?)[的]?图", r"(画|绘制|生成)[一张个幅]?.+?出来",
                    r"(能|可以|请)(画|绘制|生成|做|设计).+?吗", r"(来|整|要)(张|个).{0,5}图"]

        # 直接匹配关键词
        for kw in keywords:
            if kw in text:
                return True

        # 正则匹配更复杂的句式
        for pattern in patterns:
            if re.search(pattern, text):
                return True

        return False

    def gemini2(text):
        if not text or not isinstance(text, str):
            return False

        text = text.strip()
        if not text:
            return False

        # --- 1. 定义核心关键词 ---

        # 明确的画图动词
        drawing_verbs = ["画", "绘制", "生成", "创作", "做", "弄", "搞", "设计", "整", "出",  # 例如 "出张图"
                         "来"  # 例如 "来张图", "来个头像"
                         ]
        # 图像相关的名词 (目标)
        image_nouns = ["图", "图片", "图像", "插画", "画",  # "画"也可以是名词
                       "壁纸", "照片", "头像", "表情包", "封面", "海报", "设计稿", "效果图", "概念图", "草图", "线稿",
                       "漫画", "logo", "图标", "icon"  # 包含一些常用英文/外来词
                       ]
        # 请求/命令相关的词 (加强意图)
        request_starters = ["帮我", "给我", "请", "能不能", "可不可以", "试试", "尝试", "想看", "想要", "需要"]
        # 量词 (常与名词搭配)
        measure_words = ["张", "幅", "个", "份", "套"]

        # --- 2. 定义否定词 ---
        # 注意：否定词的位置和范围很关键
        negation_words = ["不", "别", "不要", "不是", "没有", "并非", "无须", "不用"]

        # --- 3. 定义强触发模式 (正则表达式) ---
        # 这些模式通常是明确的画图请求

        patterns = []

        # 模式组合: (请求词)? + (动词) + (量词)? + (名词)
        # 例如: "帮我画张图", "生成壁纸", "来个头像"
        verb_pattern = "|".join(map(re.escape, drawing_verbs))
        noun_pattern = "|".join(map(re.escape, image_nouns))
        starter_pattern = "|".join(map(re.escape, request_starters))
        measure_pattern = "|".join(map(re.escape, measure_words))

        # 核心模式 1: [动词] ... [名词] (允许中间有少量其他词)
        patterns.append(re.compile(rf"({verb_pattern})[\s\S]{{0,15}}({noun_pattern})"))
        # 核心模式 2: [请求词] ... [动词] ... [名词] (更强的意图)
        patterns.append(re.compile(rf"({starter_pattern})[\s\S]{{0,10}}({verb_pattern})[\s\S]{{0,15}}({noun_pattern})"))
        # 核心模式 3: [请求词]? + [动词] + [量词]? + [名词] (结构更紧凑)
        patterns.append(
            re.compile(rf"(?:{starter_pattern})?\s*({verb_pattern})\s*(?:{measure_pattern})?\s*({noun_pattern})"))
        # 核心模式 4: 特殊短语，例如 "来张/个..."
        patterns.append(re.compile(rf"(?:{starter_pattern})?\s*(来)\s*({measure_pattern})\s*({noun_pattern})"))
        patterns.append(re.compile(
            rf"(?:{starter_pattern})?\s*(来)\s*({measure_pattern})\s*([\w\s]+)"))  # 例如 "来张猫猫图", "来个赛博朋克风格的城市夜景"
        patterns.append(
            re.compile(rf"(?:{starter_pattern})?\s*(出)\s*({measure_pattern})\s*({noun_pattern})"))  # 例如 "出张图"

        # 模式 5: 描述性内容 + 要求生成/画出来
        # 例如: "一只猫在月光下，把它画出来" 或 "...，生成图片"
        # 注意: 这类模式容易误判，需要谨慎添加，这里先用简单的结尾模式
        patterns.append(
            re.compile(rf".*[，。！；]\s*({verb_pattern})\s*(?:{measure_pattern})?\s*(?:{noun_pattern}|出来|它|这个)$"))
        patterns.append(re.compile(
            rf"({verb_pattern})\s*一?\s*({measure_pattern})\s*([\w\s]+?)\s*的\s*({noun_pattern}|画)"))  # "画一张猫的图片"

        # --- 4. 检查强触发模式 ---
        match_found = False
        matched_span: Optional[Tuple[int, int]] = None

        for pattern in patterns:
            match = pattern.search(text)
            if match:
                # 初步匹配成功
                match_found = True
                matched_span = match.span()
                # print(f"Debug: Pattern matched: {pattern.pattern} -> {match.group(0)}") # Debugging line
                break  # 找到一个强模式就足够了，可以跳出

        if not match_found:
            # --- 5. 检查较弱的信号 (例如只有动词或名词，但上下文暗示) ---
            # 检查是否以 "画一个/画个..." 开头，后面跟描述
            if re.match(rf"^\s*({verb_pattern})\s*一?({measure_pattern}|\s)\s*([\w\s,.!?，。！？]+)$", text):
                # 例如 "画一个苹果", "画, 一只飞翔的鸟"
                # 需要排除 "画画" (drawing as a hobby) 这类情况
                if not re.match(r"^\s*画画", text):
                    match_found = True
                    matched_span = (0, len(text))  # 粗略标记整个文本为匹配范围

            # 检查是否包含 "画/生成/绘制 + 的 + [描述]" 结构  # 例如 "画的老虎", "生成的风景" - 可能是在问生成的图片，但也可能不是请求  # 这部分容易误判，暂时不加，除非有明确的请求词  # if re.search(rf"({verb_pattern})\s*的\s*([\w\s]+)", text) and any(starter in text for starter in request_starters):  #    match_found = True

        # --- 6. 如果没有找到任何潜在匹配，直接返回 False ---
        if not match_found or matched_span is None:
            # print("Debug: No pattern matched.") # Debugging line
            return False

        # --- 7. 否定检查 ---
        # 检查匹配到的区域附近（尤其是前面）是否有否定词

        # 设定检查窗口，例如匹配区域前 N 个字符
        window_size = 10
        start_index = max(0, matched_span[0] - window_size)
        check_window = text[start_index:matched_span[1]]  # 检查从窗口开始到匹配结束的部分

        # 提取匹配中的核心动词，用于更精确的否定判断
        core_verb_in_match = None
        if match_found and patterns:  # 确保是通过 patterns 找到的匹配
            # 尝试从第一个捕获组获取动词 (根据模式设计)
            try:
                if match and match.groups():
                    # 尝试找到第一个属于 drawing_verbs 的捕获组
                    for group in match.groups():
                        if group in drawing_verbs:
                            core_verb_in_match = group
                            break
            except IndexError:
                pass  # 某些模式可能没有捕获组或不符合预期

        # 检查否定词 + 动词的组合是否在窗口内
        for neg in negation_words:
            # 检查 1: 否定词 + 核心动词 (如果能提取到)
            if core_verb_in_match:
                neg_verb_pattern = re.compile(rf"{re.escape(neg)}\s*({re.escape(core_verb_in_match)})")
                if neg_verb_pattern.search(check_window):
                    # print(f"Debug: Negation found (neg + core_verb): {neg} + {core_verb_in_match} in '{check_window}'") # Debugging line
                    return False  # 发现否定 + 核心动词

            # 检查 2: 否定词 + 任何画图动词 (更宽松，但也可能误判)
            # 仅当否定词紧邻动词时才认为是强否定
            neg_any_verb_pattern = re.compile(rf"{re.escape(neg)}\s*({verb_pattern})")
            # 检查否定词是否出现在紧靠匹配动词的位置
            # 获取匹配到的动词在文本中的实际位置 (如果可能)
            verb_match_in_window = None
            if match and patterns:
                for i, ptn in enumerate(patterns):
                    m = ptn.search(text)
                    if m and m.span() == matched_span:  # 确认是这个 pattern 的匹配
                        verb_indices = [idx for idx, grp in enumerate(m.groups() or []) if grp in drawing_verbs]
                        if verb_indices:
                            verb_span_in_match = m.span(verb_indices[0] + 1)  # +1 因为 group(0) 是整个匹配
                            # 检查否定词是否紧邻动词前方
                            neg_check_start = max(0, verb_span_in_match[0] - len(neg) - 2)
                            neg_check_area = text[neg_check_start:verb_span_in_match[0]]
                            if neg in neg_check_area.strip():
                                # print(f"Debug: Negation found (neg adjacent to verb): {neg} near '{m.group(verb_indices[0] + 1)}'") # Debugging line
                                return False
                        break  # 找到对应的 pattern 和动词位置

            # 检查 3: 特殊否定短语
            if "不是让你画" in check_window or "不是要画" in check_window or "别画" in check_window or "不要画" in check_window:
                # print(f"Debug: Negation phrase found in '{check_window}'") # Debugging line
                return False

        # --- 8. 排除特殊非画图场景 (容易误判的) ---
        # 例如讨论画画技巧，或者引用别人的话
        # a) 讨论画画本身 ("画画很有趣", "学习画画")
        if re.search(r"(学习|讨论|关于|喜欢|爱好|技巧).{0,5}(画画|绘画|作画)", text) or re.search(r"(画画|绘画)本身",
                                                                                                  text):
            # print("Debug: Excluded - discussing drawing itself.") # Debugging line
            return False

        # b) 询问如何画 ("怎么画", "如何画") - 通常不是让AI画
        if re.search(r"(怎么|如何|怎样|步骤).{0,5}(画|绘制|生成)", text):
            # print("Debug: Excluded - asking 'how to draw'.") # Debugging line
            return False

        # c) 提及图像生成技术 ("图像生成技术", "AI画画的原理")
        if re.search(r"(图像生成|AI画画|文生图).{0,5}(技术|原理|模型|工具|软件)", text):
            # print("Debug: Excluded - discussing drawing tech.") # Debugging line
            return False

        # d) 包含引号，可能是在引用或讨论别人的请求
        #    简单处理：如果画图关键词在引号内，可能不是当前用户的直接请求
        #    注意：这个规则比较粗糙，可能误伤需要引号描述内容的情况 (如：画一个主题是"爱与和平"的画)
        #    可以考虑只排除整个请求都在引号内的情况
        # if ('"' in text or '“' in text or '”' in text or "'" in text) and matched_span:
        #    quoted_text = re.findall(r'["“](.*?)["”]', text)
        #    for quote in quoted_text:
        #        # 如果匹配到的核心内容在引号内，则可能不是直接请求
        #        if text[matched_span[0]:matched_span[1]] in quote:
        #             print("Debug: Excluded - potential quote.") # Debugging line
        #             # return False # 此规则暂时禁用，因容易误伤
        #             pass

        # --- 9. 通过所有检查，认为是画图请求 ---
        # print(f"Debug: Determined as drawing request: {text}") # Debugging line
        return True

    def deepseek(text):
        if not text or not isinstance(text, str):
            return False

        # 预处理：去除标点、空格，转换为小写
        processed = re.sub(r'[^\w\u4e00-\u9fff]', '', text.lower())

        # 常见画图请求关键词
        drawing_keywords = [  # 直接请求
            '画', '绘画', '画一张', '画一幅', '画一个', '画图', '画出来', '生成图片', '生成图像', '生成画', '生成一张',
            '生成一幅', '绘制', '绘制一张', '绘制一幅', '绘制一个', '给我画', '帮我画', '请画', '请绘制', '请生成',
            '制作图片', '制作图像', '制作画', '做一张图', '做一幅画', '设计图片', '设计图像', '设计画',

            # 间接请求
            '想要图', '想要画', '想要图片', '想要图像', '需要图', '需要画', '需要图片', '需要图像', '来张图', '来张画',
            '来张图片', '来张图像', '来幅图', '来幅画', '来幅图片', '来幅图像', '来个图', '来个画', '来个图片',
            '来个图像',

            # 英文关键词
            'draw', 'painting', 'generateimage', 'generatepicture', 'generatedrawing', 'createimage', 'createpicture',
            'createdrawing', 'makepicture', 'makeimage', 'designimage', 'designpicture']

        # 否定词（如果包含这些词可能不是画图请求）
        negative_words = ['不画', '不要画', '不想画', '不用画', '不能画', '不会画', '不需要画', '不想要画', '别画',
                          '无需画', 'nodraw', 'notdraw', 'dontdraw', 'nopicture']

        # 检查否定词
        for word in negative_words:
            if word in processed:
                return False

        # 检查画图关键词
        for word in drawing_keywords:
            if word in processed:
                return True

        # 检查"图片/图像"相关短语
        image_related = re.search(r'(生成|制作|创建|设计|想要|需要|来)(一张|一幅|一个)?(图|画|图片|图像)', processed)
        if image_related:
            return True

        # 检查AI绘画模型相关请求
        model_keywords = ['stable diffusion', 'dall', 'midjourney', 'sd', 'mj', '文生图', '图生图', 'ai绘画', 'ai画图',
                          'ai生成']
        for keyword in model_keywords:
            if keyword in text.lower():
                return True

        # 检查描述性内容（可能是在描述要画的画面）
        descriptive_phrases = [r'画面是.*', r'内容是.*', r'主题是.*', r'风格是.*', r'.*的样子', r'.*的场景',
                               r'.*的图片', r'.*的图像']
        for phrase in descriptive_phrases:
            if re.search(phrase, text):
                return True

        # 检查是否有视觉描述但无明显请求词
        visual_words = ['红色', '蓝色', '绿色', '黄色', '颜色', '色彩', '风景', '人物', '动物', '建筑', '背景', '前景',
                        '卡通', '写实', '油画', '水彩', '素描', '风格', '阳光', '夜晚', '白天', '黄昏', '早晨']
        visual_count = sum(1 for word in visual_words if word in text)
        if visual_count >= 3:  # 如果有多个视觉相关词汇
            return True

        return False

    def deepseek2(text):
        # 预处理：去除标点符号和空白，转小写
        text = re.sub(r'[^\w\u4e00-\u9fff]', '', text.lower())

        # 中英文关键词映射（动词+名词）
        keywords = {'verbs': {'画', '生成', '绘制', '创建', '设计', '制作', '给出', '输出', '呈现', 'draw', 'generate',
                              'create', 'design', 'make', 'show', 'render'},
                    'nouns': {'图', '图片', '图像', '画作', '插图', '海报', '照片', '视觉图', '壁纸', 'image',
                              'picture', 'graphic', 'artwork', 'poster', 'photo', 'drawing'},
                    'styles': {'水墨', '油画', '卡通', '像素', '3d', '写实', '水彩', '抽象', '矢量', 'minimalist',
                               'anime', 'realistic', 'sketch', 'digital'}}

        # 否定词模式（需出现在关键词前）
        negation_pattern = r'(不|没|无需|不需要|不必|不要|未曾|不想|能否|吗|？|\?)'

        # 组合否定词+关键词的正则模式
        negation_keyword_regex = re.compile(
            negation_pattern + r'.*?(' + '|'.join(keywords['verbs'] | keywords['nouns']) + r')')

        # 如果存在否定表达则直接返回False
        if negation_keyword_regex.search(text):
            return False

        # 匹配核心关键词组合
        has_verb = any(v in text for v in keywords['verbs'])
        has_noun = any(n in text for n in keywords['nouns'])
        has_style = any(s in text for s in keywords['styles'])

        # 组合逻辑：动词+(名词或风格) 或 单独名词+风格
        return (has_verb and (has_noun or has_style)) or (has_noun and has_style)

    return gemini(text), claude(text), chatgpt(text), gemini2(text), deepseek(text), deepseek2(text)


def test():
    # --- 测试用例 ---
    test_cases_positive = ["画一只可爱的猫咪", "帮我生成一张未来城市的图片", "来张风景壁纸",
                           "请绘制一个公司的logo，要求简约", "给我做个卡通头像", "生成图像：一条龙在飞翔",
                           "我想看日落的海滩景象，画出来", "设计一个游戏角色的概念图", "弄个表情包，要搞笑的",
                           "画幅山水画", "画张图，关于太空探索", "尝试画一下苹果", "来个赛博朋克风格的城市夜景",
                           "画一个红色的圆圈", "我想要一幅梵高风格的星空画", "绘制草图：一个新的建筑设计", ]

    test_cases_negative = ["你画画真好看", "图像生成技术现在很厉害", "我不需要图片", "这张图是怎么画的？",
                           "请生成一份销售报告", "我不是让你画画，我是让你写诗", "别画了，我们聊点别的", "关于绘画的技巧",
                           "这个模型可以生成图像吗？", "我学习画画很久了", "不要生成图片", "我没有让你画图",
                           "请不要给我画画", "你刚才画的图不好看", "AI画画的原理是什么？", "讲个笑话吧",
                           "今天天气怎么样", "解释一下这个代码", "写一首关于春天的诗", ]

    test_cases = test_cases_positive + test_cases_negative
    labels = [True] * len(test_cases_positive) + [False] * len(
        test_cases_negative)  # True for positive, False for negative

    model_names = ["gemini", "claude", "chatgpt", "gemini2", "deepseek", "deepseek2"]
    model_results = {name: [] for name in model_names}
    case_correctness = [[] for _ in range(len(test_cases))]

    # Run tests and collect results
    for i, case in enumerate(test_cases):
        results = drawing_intention_judgement(case)
        for j, model_name in enumerate(model_names):
            model_results[model_name].append(results[j])
            case_correctness[i].append(results[j] == labels[i])

    # Calculate model accuracy
    model_accuracies = {}
    for model_name in model_names:
        correct_count = sum(1 for i, result in enumerate(model_results[model_name]) if result == labels[i])
        model_accuracies[model_name] = correct_count / len(test_cases)

    # Calculate case accuracy
    case_accuracies = []
    for i in range(len(test_cases)):
        correct_count = sum(1 for correct in case_correctness[i] if correct)
        case_accuracies.append(correct_count / len(model_names))

    # Print results
    print("\n模型判断正确率:")
    for model_name, accuracy in model_accuracies.items():
        print(f"{model_name}: {accuracy:.4f}")

    print("\n测试用例判断正确率:")
    for i, accuracy in enumerate(case_accuracies):
        if accuracy < 0.5:
            color_code = "\033[91m"  # 红色
        elif accuracy < 0.8:
            color_code = "\033[93m"  # 黄色
        else:
            color_code = "\033[92m"  # 绿色
        reset_code = "\033[0m"  # 重置颜色

        print(f"测试用例 {i + 1}: {color_code}{accuracy:.4f}{reset_code}")
