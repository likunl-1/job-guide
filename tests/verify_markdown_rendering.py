"""
验证HTML报告的Markdown渲染效果
"""

import sys
import os

workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
sys.path.insert(0, workspace_path)
sys.path.insert(0, os.path.join(workspace_path, "src"))

from src.tools.html_report_tool import generate_html_report
import json

# 简化的测试数据
user_profile = {
    "name": "测试同学",
    "education": "211财经院校 金融学院 研一",
    "major": "金融学",
    "grade": "前30%",
    "skills": ["Python", "金融学"],
    "expectations": "稳定工作"
}

# 简化的测试内容，包含各种Markdown元素
test_content = """
## 测试标题

这是一个测试段落，用于验证Markdown渲染。

### 列表测试
- 无序列表项1
- 无序列表项2
  - 嵌套列表项
- 无序列表项3

1. 有序列表项1
2. 有序列表项2
3. 有序列表项3

### 表格测试
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |
| D   | E   | F   |

### 代码块测试
```python
print("Hello, World!")
```

### 引用测试
> 这是一段引用内容

### 强调测试
**加粗文本**
*斜体文本*
`行内代码`

---

分割线
"""

html_report_func = generate_html_report.func

print("🧪 测试Markdown渲染功能...")
result = html_report_func(
    user_profile=json.dumps(user_profile),
    employment_analysis=test_content,
    recommendations=test_content,
    action_plan=test_content,
    report_type="general",
    output_filename="test_markdown_elements.html"
)

print("\n✅ 测试完成！")
print(result)
print("\n📄 请在浏览器中打开 'assets/reports/test_markdown_elements.html' 查看")
print("   检查以下元素是否正确渲染：")
print("   - 标题（h1, h2, h3）")
print("   - 列表（有序、无序、嵌套）")
print("   - 表格")
print("   - 代码块")
print("   - 引用")
print("   - 强调（加粗、斜体）")
print("   - 分割线")
