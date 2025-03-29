import pandas as pd
import re
import os
from pathlib import Path

def count_chinese(text):
    """统计中文字符数量（排除符号）"""
    if pd.isna(text):
        return 0
    return len(re.findall(r'[\u4e00-\u9fff]', str(text)))

def sanitize_sheet_name(name):
    """生成合法工作表名称"""
    invalid_chars = [':', '\\', '/', '?', '*', '[', ']']
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name[:31]

def process_excel(file_path):
    """处理单个Excel文件"""
    try:
        df = pd.read_excel(file_path, engine='openpyxl', header=None)
        
        # 处理首行
        new_header = ["标题", "内容"] + [''] * (df.shape[1]-2)
        df.iloc[0] = new_header
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)

        # 验证目标列
        if "内容" not in df.columns:
            print(f"跳过 {file_path}：缺少'内容'列")
            return

        # 过滤数据
        df['中文字数'] = df["内容"].apply(count_chinese)
        df_filtered = df[df['中文字数'] >= 50].drop(columns=['中文字数'])

        # 生成输出路径
        output_path = str(file_path).replace('.xlsx', '_processed.xlsx')
        
        # 生成工作表名称
        base_name = Path(file_path).stem  # 获取不带扩展的文件名
        sheet_name = sanitize_sheet_name(base_name)

        # 保存结果
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, index=False, sheet_name=sheet_name)
        
        print(f"成功处理：{Path(file_path).name} -> {Path(output_path).name}")

    except Exception as e:
        print(f"处理失败：{file_path}\n错误原因：{str(e)}")

if __name__ == "__main__":
    # 设置目标目录
    target_dir = r"F:\科技项目\鸿鹄科技项目\质子AI(AAAA20250314ZZ)\知识库"
    
    # 遍历目录中的Excel文件
    processed_count = 0
    for file in Path(target_dir).glob('*.xlsx'):
        if not file.name.endswith('_processed.xlsx'):  # 跳过已处理的文件
            process_excel(file)
            processed_count += 1
    
    print(f"\n处理完成，共处理 {processed_count} 个文件")
    print("注：输出文件与原文件在同一目录，文件名添加'_processed'后缀")