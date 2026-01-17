# 生成报告目录

本目录包含AI Agent生成的HTML格式就业指导报告。

## 📊 示例报告列表

### 🎓 学生案例报告
1. **迷茫学生问答报告** (`迷茫学生问答报告.html`)
   - 大小: 32KB
   - 类型: 学生职业规划报告
   - 生成时间: 2025-01-15
   - 说明: 针对迷茫学生的职业规划建议和指导

2. **李小硕就业报告** (`li_xiaoshuo_employment_report.html`)
   - 大小: 36KB
   - 类型: 个人就业分析报告
   - 说明: 个人简历分析和就业建议

### 📈 金融市场报告
3. **金融市场报告** (`金融市场报告.html`)
   - 大小: 28KB
   - 类型: 行业分析报告
   - 生成时间: 2025-01-15
   - 说明: 金融市场就业趋势分析

### 📝 综合报告
4. **综合Markdown报告** (`comprehensive_report_markdown.html`)
   - 大小: 32KB
   - 类型: 综合分析报告
   - 说明: 包含多种内容格式的完整报告

### 🧪 测试报告
以下报告用于功能测试和演示：
- `test_employment_report.html` - 就业报告测试 (14KB)
- `test_markdown_elements.html` - Markdown元素测试 (25KB)
- `test_markdown_rendering.html` - Markdown渲染测试 (26KB)

---

## 🔧 技术说明

### 报告生成工具
- **工具文件**: `src/tools/html_report_tool.py`
- **输出目录**: `assets/reports/`
- **支持格式**: HTML (带CSS动画和交互)

### 报告特性
- ✅ 响应式设计，支持移动端
- ✅ 包含ECharts数据可视化图表
- ✅ 支持词云展示
- ✅ Markdown内容渲染
- ✅ 代码高亮显示
- ✅ 动画效果和交互

---

## 📌 使用说明

### 查看报告
直接在浏览器中打开HTML文件即可查看：
```bash
# Linux/Mac
open assets/reports/迷茫学生问答报告.html

# Windows
start assets/reports/迷茫学生问答报告.html
```

### 生成新报告
通过AI Agent生成新报告，文件会自动保存到此目录。

### 清理测试报告
测试报告可以删除，不影响系统功能：
```bash
rm assets/reports/test_*.html
```

---

## ⚠️ 注意事项

1. **勿删除核心报告**: 迷茫学生问答报告、金融市场报告、李小硕就业报告、综合Markdown报告是重要的示例报告
2. **定期清理**: test_开头的测试报告可以定期删除
3. **备份重要**: 建议将重要的案例报告备份到云端或版本控制
