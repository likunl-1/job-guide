"""
招聘数据API集成示例

展示如何集成真实的招聘数据API
以Boss直聘API为例（实际集成需要申请API Key）

注意：本文件为示例，实际使用前请：
1. 申请相应平台的API Key
2. 阅读平台的使用文档
3. 遵守平台的调用限制和规则
"""

import os
import requests
import time
from typing import List, Dict, Optional
from coze_coding_utils.runtime_ctx.context import Context, default_headers


class RecruitmentAPIClient:
    """
    招聘数据API客户端（示例）

    支持多个招聘平台的数据获取
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化API客户端

        Args:
            config: API配置字典，包含各平台的API Key和端点
        """
        self.config = config or {}
        self.cache = {}  # 简单缓存
        self.last_call_time = {}  # 记录最后一次调用时间（用于限流）

    def search_jobs(
        self,
        keyword: str,
        city: str = "",
        platform: str = "boss_zhipin",
        ctx: Optional[Context] = None
    ) -> List[Dict]:
        """
        搜索招聘职位

        Args:
            keyword: 搜索关键词
            city: 城市（可选）
            platform: 使用的平台（boss_zhipin/lagou/liepin/third_party）
            ctx: 上下文对象

        Returns:
            职位列表
        """
        # 检查平台是否启用
        platform_config = self.config.get(platform)
        if not platform_config or not platform_config.get("enabled"):
            raise Exception(f"平台 {platform} 未启用或未配置")

        # 检查缓存
        cache_key = f"{platform}:{keyword}:{city}"
        if self.config.get("common", {}).get("cache_enabled", False):
            if cache_key in self.cache:
                cached_data, cache_time = self.cache[cache_key]
                cache_ttl = self.config.get("common", {}).get("cache_ttl", 3600)
                if time.time() - cache_time < cache_ttl:
                    print(f"从缓存返回数据: {cache_key}")
                    return cached_data

        # 限流检查
        self._check_rate_limit(platform)

        # 根据平台调用不同的API
        if platform == "boss_zhipin":
            jobs = self._search_boss_zhipin(keyword, city, ctx)
        elif platform == "lagou":
            jobs = self._search_lagou(keyword, city, ctx)
        elif platform == "liepin":
            jobs = self._search_liepin(keyword, city, ctx)
        elif platform == "third_party":
            jobs = self._search_third_party(keyword, city, ctx)
        else:
            raise Exception(f"不支持的平台: {platform}")

        # 缓存结果
        if self.config.get("common", {}).get("cache_enabled", False):
            self.cache[cache_key] = (jobs, time.time())

        return jobs

    def _check_rate_limit(self, platform: str):
        """
        检查并执行限流

        Args:
            platform: 平台名称
        """
        platform_config = self.config.get(platform, {})
        rate_limit = platform_config.get("rate_limit", 100)  # 默认每分钟100次

        # 记录最后一次调用时间
        last_call = self.last_call_time.get(platform, 0)
        time_since_last = time.time() - last_call

        # 如果调用间隔太小，则等待
        min_interval = 60.0 / rate_limit  # 每分钟最大请求数 -> 每次请求最小间隔
        if time_since_last < min_interval:
            sleep_time = min_interval - time_since_last
            print(f"限流中，等待 {sleep_time:.2f} 秒...")
            time.sleep(sleep_time)

        # 更新最后一次调用时间
        self.last_call_time[platform] = time.time()

    def _search_boss_zhipin(self, keyword: str, city: str, ctx: Optional[Context]) -> List[Dict]:
        """
        搜索Boss直聘职位（示例）

        Args:
            keyword: 搜索关键词
            city: 城市
            ctx: 上下文对象

        Returns:
            职位列表
        """
        api_key = self.config["boss_zhipin"]["api_key"]
        endpoint = self.config["boss_zhipin"]["endpoint"]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        if ctx:
            headers.update(default_headers(ctx))

        params = {
            "keyword": keyword,
            "city": city if city else "全国",
            "page": 1,
            "pageSize": 20,
        }

        timeout = self.config.get("common", {}).get("request_timeout", 10)
        max_retries = self.config.get("common", {}).get("max_retries", 3)
        retry_delay = self.config.get("common", {}).get("retry_delay", 2)

        for attempt in range(max_retries):
            try:
                response = requests.get(
                    endpoint,
                    params=params,
                    headers=headers,
                    timeout=timeout
                )

                if response.status_code == 200:
                    data = response.json()
                    # 根据实际API返回格式解析
                    jobs = self._parse_boss_zhipin_response(data)
                    return jobs
                else:
                    raise Exception(f"API返回错误: {response.status_code}")

            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"请求失败，{retry_delay}秒后重试... ({attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                else:
                    raise Exception(f"API请求失败: {str(e)}")

        return []

    def _parse_boss_zhipin_response(self, data: Dict) -> List[Dict]:
        """
        解析Boss直聘API响应（示例）

        Args:
            data: API返回的原始数据

        Returns:
            解析后的职位列表
        """
        # 根据实际API返回格式调整
        # 以下是示例格式
        jobs = []

        raw_jobs = data.get("jobList", data.get("data", []))

        for job in raw_jobs:
            parsed_job = {
                "title": job.get("jobName", "未知职位"),
                "company": job.get("brandName", "未知公司"),
                "salary": job.get("salaryDesc", "面议"),
                "location": job.get("cityName", "未知"),
                "experience": job.get("jobExperience", "未知"),
                "education": job.get("jobDegree", "未知"),
                "publish_time": job.get("createTime", "未知"),
                "url": f"https://www.zhipin.com/job_detail/{job.get('encryptJobId')}",
                "description": job.get("jobDescription", ""),
            }
            jobs.append(parsed_job)

        return jobs

    def _search_lagou(self, keyword: str, city: str, ctx: Optional[Context]) -> List[Dict]:
        """
        搜索拉勾网职位（示例）

        注意：拉勾网API通常需要企业资质
        """
        # 类似实现...
        raise NotImplementedError("拉勾网API集成需要申请企业资质")

    def _search_liepin(self, keyword: str, city: str, ctx: Optional[Context]) -> List[Dict]:
        """
        搜索猎聘职位（示例）
        """
        # 类似实现...
        raise NotImplementedError("猎聘API集成需要申请API Key")

    def _search_third_party(self, keyword: str, city: str, ctx: Optional[Context]) -> List[Dict]:
        """
        使用第三方数据服务（示例）
        """
        api_key = self.config["third_party"]["api_key"]
        endpoint = self.config["third_party"]["endpoint"]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        params = {
            "keyword": keyword,
            "city": city,
            "limit": 20,
        }

        response = requests.get(endpoint, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("jobs", [])
        else:
            raise Exception(f"第三方API返回错误: {response.status_code}")


# ===== 使用示例 =====

def example_usage():
    """
    使用示例
    """

    # 1. 配置API（从环境变量或配置文件读取）
    config = {
        "boss_zhipin": {
            "enabled": True,
            "api_key": os.getenv("BOSS_ZHIPIN_API_KEY", "your_api_key_here"),
            "endpoint": "https://api.zhipin.com/job/search",
            "rate_limit": 100,
        },
        "common": {
            "cache_enabled": True,
            "cache_ttl": 3600,
            "request_timeout": 10,
            "max_retries": 3,
            "retry_delay": 2,
        },
    }

    # 2. 创建客户端
    client = RecruitmentAPIClient(config)

    # 3. 搜索职位
    try:
        jobs = client.search_jobs(
            keyword="前端开发",
            city="北京",
            platform="boss_zhipin"
        )

        # 4. 处理结果
        print(f"找到 {len(jobs)} 个职位")
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job['title']}")
            print(f"   公司：{job['company']}")
            print(f"   薪资：{job['salary']}")
            print(f"   地点：{job['location']}")
            print(f"   链接：{job['url']}")

    except Exception as e:
        print(f"搜索失败: {e}")


# ===== 在Agent中使用的示例 =====

def get_real_jobs_from_api(keyword: str, ctx: Context) -> str:
    """
    在Agent工具中获取真实招聘数据

    Args:
        keyword: 搜索关键词
        ctx: 上下文对象

    Returns:
        格式化后的职位信息
    """
    # 从环境变量读取配置
    api_key = os.getenv("RECRUITMENT_API_KEY")
    api_endpoint = os.getenv("RECRUITMENT_API_ENDPOINT")

    if not api_key or not api_endpoint:
        raise Exception("未配置招聘数据API")

    # 创建配置
    config = {
        "boss_zhipin": {
            "enabled": True,
            "api_key": api_key,
            "endpoint": api_endpoint,
            "rate_limit": 100,
        },
        "common": {
            "cache_enabled": True,
            "cache_ttl": 3600,
            "request_timeout": 10,
            "max_retries": 3,
            "retry_delay": 2,
        },
    }

    # 创建客户端并搜索
    client = RecruitmentAPIClient(config)

    try:
        jobs = client.search_jobs(
            keyword=keyword,
            platform="boss_zhipin",
            ctx=ctx
        )

        # 格式化结果
        lines = []
        lines.append(f"### 📝 找到 {len(jobs)} 个相关岗位")
        lines.append("")
        lines.append("**数据来源**：招聘平台API")
        lines.append("**数据时效**：实时/准实时")
        lines.append("")

        for i, job in enumerate(jobs, 1):
            lines.append(f"**{i}. {job['title']}**")
            lines.append(f"- 公司：{job['company']}")
            lines.append(f"- 薪资：{job['salary']}")
            lines.append(f"- 地点：{job['location']}")
            lines.append(f"- 经验：{job['experience']}")
            lines.append(f"- 学历：{job['education']}")
            lines.append(f"- 发布时间：{job['publish_time']}")
            lines.append(f"- 查看详情：{job['url']}")
            lines.append("")

        return "\n".join(lines)

    except Exception as e:
        raise Exception(f"获取招聘数据失败: {str(e)}")


if __name__ == "__main__":
    example_usage()
