"""
保存爬取的数据到 CSV/Excel 文件
"""

import pandas as pd
import datetime
import os


class DataSaver(object):
    """数据保存工具，支持 CSV 和 Excel 格式"""
    
    def __init__(self, keyword, citys, save_dir="assets/jobs_data"):
        """
        初始化数据保存器
        
        Args:
            keyword: 搜索关键词
            citys: 城市列表
            save_dir: 保存目录
        """
        self.T = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d_%H%M")
        self.keyword = keyword
        self.save_dir = save_dir
        
        # 处理城市名称
        if len(citys) == 1:
            self.city = citys[0]
        elif len(citys) > 1:
            self.city = "&".join(citys)
        else:
            self.city = "全国"
        
        # 创建文件名
        self.file_name = f"{self.keyword}_{self.city}_招聘数据"
        self.file_path_csv = os.path.join(save_dir, f"{self.file_name}.csv")
        self.file_path_excel = os.path.join(save_dir, f"{self.file_name}.xlsx")
        
        # 确保目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 初始化数据列表
        self.data_list = []
        
    def insert_data(self, data):
        """
        插入一条数据
        
        Args:
            data: 字典格式的数据
        """
        self.data_list.append(data)
        print(f"成功插入一条信息，当前共 {len(self.data_list)} 条")
    
    def save_to_csv(self):
        """保存数据到 CSV 文件"""
        if not self.data_list:
            print("没有数据可保存")
            return
        
        try:
            df = pd.DataFrame(self.data_list)
            df.to_csv(self.file_path_csv, index=False, encoding='utf-8-sig')
            print(f"成功保存到 CSV 文件: {self.file_path_csv}")
            return self.file_path_csv
        except Exception as e:
            print(f"保存 CSV 文件失败: {e}")
            return None
    
    def save_to_excel(self):
        """保存数据到 Excel 文件"""
        if not self.data_list:
            print("没有数据可保存")
            return
        
        try:
            df = pd.DataFrame(self.data_list)
            df.to_excel(self.file_path_excel, index=False)
            print(f"成功保存到 Excel 文件: {self.file_path_excel}")
            return self.file_path_excel
        except Exception as e:
            print(f"保存 Excel 文件失败: {e}")
            return None
    
    def save(self):
        """保存数据（默认保存为 Excel 格式）"""
        return self.save_to_excel()
    
    def get_data_count(self):
        """获取当前数据条数"""
        return len(self.data_list)
    
    def clear_data(self):
        """清空数据"""
        self.data_list = []
        print("数据已清空")


if __name__ == '__main__':
    # 测试代码
    test_data = {
        '职位名称': '淘宝/天猫运营',
        '公司名称': '深圳市东健宇电子有限公司',
        '薪资': '4.5-6千/月',
        '工作地点': '深圳',
        '发布时间': '2024-01-15',
        '招聘链接': 'http://jobs.51job.com/shenzhen/86494101.html?s=01&t=0',
        '公司链接': 'http://jobs.51job.com/all/co2628963.html'
    }
    
    saver = DataSaver("爬虫", ["深圳", "武汉"])
    saver.insert_data(test_data)
    saver.insert_data(test_data)
    
    print(f"\n数据条数: {saver.get_data_count()}")
    saver.save()
