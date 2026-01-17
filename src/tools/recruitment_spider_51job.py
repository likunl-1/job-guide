"""
前程无忧（51job）招聘信息爬虫工具
支持通过关键词和城市搜索职位信息
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from langchain.tools import tool

from tools.citynum import city_to_num
from tools.data_saver import DataSaver


@tool
def search_51job(
    keyword: str,
    city: str = "深圳",
    max_pages: int = 3
) -> str:
    """
    从前程无忧（51job）爬取招聘信息
    
    Args:
        keyword: 搜索关键词，如"Python开发"、"数据分析师"等
        city: 城市名称，如"深圳"、"北京"、"上海"等
        max_pages: 最大爬取页数（默认3页，防止数据过多）
    
    Returns:
        爬取结果的摘要信息，包括数据条数、保存路径等
    
    Examples:
        >>> search_51job("Python开发", "深圳", 2)
        >>> search_51job("数据分析师", "北京", 5)
    """
    # 请求头
    headers = {
        "Host": "search.51job.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # 获取城市代码
        citys = [city]
        citynum = city_to_num.get_citynum(citys)
        
        if citynum == "040000":
            return f"⚠️ 无法匹配城市【{city}】，将使用默认城市【深圳】"
        
        # 构造搜索 URL
        search_url = (
            f"http://search.51job.com/jobsearch/search_result.php?"
            f"fromJs=1&jobarea={quote(citynum)}&keyword={quote(keyword)}"
            f"&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9"
        )
        
        # 初始化数据保存器
        saver = DataSaver(keyword, citys)
        
        # 开始爬取
        total_jobs = 0
        current_page = 0
        current_url = search_url
        
        while current_page < max_pages:
            print(f"\n正在爬取第 {current_page + 1} 页...")
            
            try:
                # 发送请求
                response = requests.get(current_url, headers=headers, timeout=10)
                response.encoding = "gbk"
                
                # 解析 HTML
                soup = BeautifulSoup(response.text, "lxml")
                
                # 获取职位信息（跳过标题行）
                jobs = soup.select("#resultList > div.el")[1:]
                
                if not jobs:
                    print("本页没有职位信息，停止爬取")
                    break
                
                # 提取职位信息
                page_jobs = 0
                for job in jobs:
                    try:
                        data = {}
                        
                        # 职位名称和链接
                        job_info = job.select("p.t1")[0]
                        data["职位名称"] = job_info.text.strip()
                        job_link_tag = job_info.select("span > a")
                        if job_link_tag:
                            data["招聘链接"] = job_link_tag[0].get("href", "")
                        else:
                            data["招聘链接"] = ""
                        
                        # 公司名称和链接
                        company_info = job.select("span.t2")[0]
                        data["公司名称"] = company_info.text.strip()
                        company_link_tag = company_info.select("a")
                        if company_link_tag:
                            data["公司链接"] = company_link_tag[0].get("href", "")
                        else:
                            data["公司链接"] = ""
                        
                        # 工作地点
                        location_tag = job.select("span.t3")
                        data["工作地点"] = location_tag[0].text.strip() if location_tag else ""
                        
                        # 薪资
                        salary_tag = job.select("span.t4")
                        data["薪资"] = salary_tag[0].text.strip() if salary_tag else "面议"
                        
                        # 发布时间
                        date_tag = job.select("span.t5")
                        data["发布时间"] = date_tag[0].text.strip() if date_tag else ""
                        
                        # 保存数据
                        saver.insert_data(data)
                        total_jobs += 1
                        page_jobs += 1
                        
                    except Exception as e:
                        print(f"解析职位信息时出错: {e}")
                        continue
                
                print(f"第 {current_page + 1} 页成功爬取 {page_jobs} 个职位")
                
                # 尝试获取下一页链接
                try:
                    next_link_tag = soup.select("li.bk")[-1].select("a")
                    if not next_link_tag:
                        print("无法获取下一页链接，停止爬取")
                        break
                    
                    next_link = next_link_tag[0].get("href")
                    
                    if next_link is None:
                        print("已到达最后一页，停止爬取")
                        break
                    
                    if "javascript:" in next_link:
                        print("已到达最后一页，停止爬取")
                        break
                    
                    current_url = next_link
                    current_page += 1
                    time.sleep(1)  # 延迟，避免请求过快
                except:
                    print("无法获取下一页链接，停止爬取")
                    break
                    
            except requests.RequestException as e:
                print(f"请求出错: {e}")
                break
            except Exception as e:
                print(f"爬取出错: {e}")
                break
        
        # 保存数据
        saved_file = saver.save()
        
        # 生成返回结果
        result = f"""
## 📊 爬取结果摘要

**搜索关键词**: {keyword}
**搜索城市**: {city}
**爬取页数**: {current_page + 1} 页
**数据条数**: {total_jobs} 条

**保存路径**: {saved_file if saved_file else '保存失败'}

### 🔍 数据字段
- 职位名称
- 公司名称
- 薪资
- 工作地点
- 发布时间
- 招聘链接
- 公司链接

### ✅ 说明
数据已保存到 `assets/jobs_data/` 目录，可以使用 `read_local_jobs` 工具读取数据。
"""
        return result
        
    except Exception as e:
        return f"❌ 爬取失败: {str(e)}\n\n请检查网络连接或稍后重试。"


# 如果直接运行此文件，可以测试爬虫
if __name__ == '__main__':
    print("测试前程无忧爬虫...")
    result = search_51job("Python开发", "深圳", 1)
    print(result)
