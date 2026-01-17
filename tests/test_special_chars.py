#!/usr/bin/env python3
"""
测试词云文件名中的特殊字符处理
"""

import os
import re

def sanitize_filename(filename):
    """
    过滤文件名中的特殊字符，避免系统解析错误

    Args:
        filename: 原始文件名

    Returns:
        处理后的安全文件名
    """
    safe_filename = filename

    # 替换或移除特殊字符
    safe_filename = safe_filename.replace(" ", "_")
    safe_filename = safe_filename.replace("-", "_")
    safe_filename = safe_filename.replace("/", "_")
    safe_filename = safe_filename.replace("\\", "_")
    safe_filename = safe_filename.replace(":", "_")
    safe_filename = safe_filename.replace("*", "_")
    safe_filename = safe_filename.replace("?", "_")
    safe_filename = safe_filename.replace('"', "_")
    safe_filename = safe_filename.replace("<", "_")
    safe_filename = safe_filename.replace(">", "_")
    safe_filename = safe_filename.replace("|", "_")

    # 移除连续的下划线
    safe_filename = re.sub(r'_+', '_', safe_filename)

    # 移除首尾的下划线
    safe_filename = safe_filename.strip('_')

    return safe_filename


# 测试用例
test_cases = [
    "数据分析/挖掘 - 技能需求词云.png",
    "产品经理 - 技能需求词云.png",
    "前端开发工程师 - 技能需求词云.png",
    "Java后端开发工程师 - 技能需求词云.png",
    "金融学研究生 - 就业市场热点词云.png",
    "互联网行业 - 招聘公司热度词云.png",
    "AI产品经理 - 技能需求词云.png",
    "Python:高级开发 - 技能需求词云.png",
    "测试*特殊?字符.png",
    "测试\"引号<符>号|.png",
    "  多个  空格  和___下划线  .png"
]

print("="*60)
print("🧪 测试特殊字符处理功能")
print("="*60)

all_passed = True
for i, original in enumerate(test_cases, 1):
    sanitized = sanitize_filename(original)

    # 检查是否还有非法字符
    illegal_chars = [' ', '-', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
    has_illegal = any(char in sanitized for char in illegal_chars)

    # 检查是否有连续下划线
    has_consecutive = '__' in sanitized

    # 检查首尾是否有下划线
    has_leading_underscore = sanitized.startswith('_')
    has_trailing_underscore = sanitized.endswith('_')

    passed = not (has_illegal or has_consecutive or has_leading_underscore or has_trailing_underscore)

    status = "✅ 通过" if passed else "❌ 失败"
    if not passed:
        all_passed = False
        issues = []
        if has_illegal:
            issues.append("仍有非法字符")
        if has_consecutive:
            issues.append("有连续下划线")
        if has_leading_underscore or has_trailing_underscore:
            issues.append("首尾有下划线")
        print(f"{i}. {status} - {original}")
        print(f"   结果: {sanitized}")
        print(f"   问题: {', '.join(issues)}\n")
    else:
        print(f"{i}. {status} - {original}")
        print(f"   结果: {sanitized}\n")

print("="*60)
if all_passed:
    print("✅ 所有测试用例通过！")
else:
    print("❌ 部分测试用例失败！")
print("="*60)

# 测试Windows和Linux文件系统限制
print("\n📋 文件系统限制检查")
print("="*60)

long_filename = "a" * 200 + ".png"
safe_long = sanitize_filename(long_filename)
print(f"超长文件名测试:")
print(f"  原始长度: {len(long_filename)}")
print(f"  处理后长度: {len(safe_long)}")

# 检查Windows保留名称
reserved_names = ['CON', 'PRN', 'AUX', 'NUL',
                  'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                  'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']

print(f"\n保留名称检查:")
print(f"  保留名称列表: {', '.join(reserved_names[:5])}...")

# 模拟处理保留名称
for reserved in reserved_names[:3]:
    test_name = f"{reserved}.png"
    safe_name = sanitize_filename(test_name)
    print(f"  {test_name} -> {safe_name}")

print("\n✅ 测试完成！")
