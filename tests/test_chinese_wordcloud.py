#!/usr/bin/env python3
"""
测试中文字体词云生成
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.font_manager as fm

# 测试字体路径
font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'

print("📝 测试中文字体词云生成...")
print(f"字体路径: {font_path}")
print(f"字体存在: {os.path.exists(font_path)}")

# 测试关键词（包含中文和英文）
test_words = {
    "数据分析": 100,
    "机器学习": 90,
    "Python": 95,
    "深度学习": 85,
    "人工智能": 80,
    "大数据": 82,
    "自然语言处理": 68,
    "计算机视觉": 65,
    "推荐系统": 60,
    "算法": 88,
    "数据挖掘": 78,
    "数据可视化": 72,
    "Spark": 55,
    "Hadoop": 50,
    "TensorFlow": 60,
    "PyTorch": 58
}

print(f"\n📊 测试关键词数量: {len(test_words)}")

# 创建词云
try:
    wordcloud = WordCloud(
        width=1200,
        height=800,
        background_color='white',
        font_path=font_path,  # 使用中文字体
        max_words=50,
        relative_scaling=0.5,
        min_font_size=10,
        colormap='viridis',
        prefer_horizontal=0.9,
        scale=2
    ).generate_from_frequencies(test_words)

    print("✅ 词云生成成功！")

    # 创建图表
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')

    # 设置标题（使用中文字体）
    title_font_prop = fm.FontProperties(fname=font_path)
    ax.set_title("中文字体测试词云图", fontsize=16, fontweight='bold', pad=20,
                fontproperties=title_font_prop)

    plt.tight_layout(pad=0)

    # 保存图片
    output_path = "assets/charts/test_chinese_wordcloud.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"✅ 词云图已保存到: {output_path}")
    print(f"📁 文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")

    # 验证图片文件
    if os.path.exists(output_path):
        print("✅ 图片文件验证成功！")
        print(f"\n💡 提示: 请打开 {output_path} 查看中文是否正确显示")
        print("   如果中文显示为方框 □□□，说明字体配置仍有问题")
        print("   如果中文正常显示，说明字体配置成功！")
    else:
        print("❌ 图片文件保存失败！")

except Exception as e:
    print(f"❌ 词云生成失败: {str(e)}")
    import traceback
    traceback.print_exc()

# 输出系统字体信息
print("\n" + "="*60)
print("📋 系统中文字体信息")
print("="*60)
chinese_fonts = [f for f in fm.fontManager.ttflist if 'zh' in f.fname.lower() or 'chinese' in f.name.lower()]
print(f"找到 {len(chinese_fonts)} 个中文字体:")
for font in chinese_fonts[:10]:
    print(f"  - {font.name}: {font.fname}")

print("\n✅ 测试完成！")
