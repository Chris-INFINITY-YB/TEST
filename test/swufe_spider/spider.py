import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
import time
import re

class SWUFESpider:
    def __init__(self):
        self.base_url = "https://jinrong.swufe.edu.cn"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_page_content(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            # 尝试不同的编码方式
            encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
            content = None
            
            for encoding in encodings:
                try:
                    response.encoding = encoding
                    content = response.text
                    # 如果解码成功，打印编码信息
                    print(f"成功使用 {encoding} 解码页面")
                    break
                except:
                    continue
            
            if content and response.status_code == 200:
                return content
            else:
                print(f"请求失败，状态码：{response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def parse_news(self, html_content):
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'lxml')
        news_items = []
        
        try:
            # 1. 获取首页新闻列表
            print("\n开始解析首页新闻...")
            
            # 查找所有可能的新闻容器
            news_containers = []
            
            # 查找底部新闻区域
            bottom_grids = soup.find_all('div', class_=['bottom-grid', 'n_left', 'n_right'])
            if bottom_grids:
                news_containers.extend(bottom_grids)
            
            # 查找其他可能的新闻区域
            other_containers = soup.find_all(['div', 'section'], class_=['news-list', 'list', 'content-list', 'news', 'article-list'])
            if other_containers:
                news_containers.extend(other_containers)
            
            # 查找所有新闻链接
            for container in news_containers:
                news_links = container.find_all('a', href=True)
                print(f"\n在容器 {container.get('class', ['unknown'])} 中找到 {len(news_links)} 个链接")
                
                for link in news_links:
                    try:
                        title = link.text.strip()
                        href = link.get('href', '')
                        
                        # 处理相对URL
                        if href and not href.startswith('http'):
                            href = self.base_url + href if href.startswith('/') else self.base_url + '/' + href
                        
                        # 尝试获取日期
                        date = ''
                        # 1. 查找相邻的日期元素
                        date_element = (
                            link.find_next('span', class_=['date', 'time']) or
                            link.find_next('div', class_=['date', 'time']) or
                            link.find_next('span', string=re.compile(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}'))
                        )
                        if date_element:
                            date = date_element.text.strip()
                        
                        # 2. 从链接文本中提取日期
                        if not date:
                            date_match = re.search(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', title)
                            if date_match:
                                date = date_match.group()
                                title = title.replace(date, '').strip()
                        
                        # 只添加有标题且看起来像新闻的链接
                        if title and len(title) > 2 and not any(x in title for x in ['首页', '返回', '更多']):
                            news_items.append({
                                'title': title,
                                'link': href,
                                'date': date
                            })
                            print(f"找到新闻: {title} ({date})")
                    except Exception as e:
                        print(f"解析新闻项时出错: {str(e)}")
                        continue
            
            # 2. 获取通知公告页面内容
            print("\n开始获取通知公告页面...")
            notice_url = "https://jinrong.swufe.edu.cn/szdw/tzgg.htm"
            notice_content = self.get_page_content(notice_url)
            if notice_content:
                notice_soup = BeautifulSoup(notice_content, 'lxml')
                
                # 查找通知列表容器
                notice_list = notice_soup.find('div', class_='list')
                if notice_list:
                    notice_items = notice_list.find_all('li')
                    print(f"在通知公告页面找到 {len(notice_items)} 条通知")
                    
                    for item in notice_items:
                        try:
                            link = item.find('a')
                            if link:
                                title = link.text.strip()
                                href = link.get('href', '')
                                
                                if href and not href.startswith('http'):
                                    href = self.base_url + href if href.startswith('/') else self.base_url + '/' + href
                                
                                # 获取日期
                                date = ''
                                date_span = item.find('span', class_='date')
                                if date_span:
                                    date = date_span.text.strip()
                                
                                if title and len(title) > 2:
                                    news_items.append({
                                        'title': title,
                                        'link': href,
                                        'date': date
                                    })
                                    print(f"找到通知: {title} ({date})")
                        except Exception as e:
                            print(f"解析通知项时出错: {str(e)}")
                            continue
                else:
                    print("未找到通知列表容器")
            
            print(f"\n成功解析到 {len(news_items)} 条新闻和通知")
        except Exception as e:
            print(f"解析页面时出错: {str(e)}")
        
        return news_items

    def save_to_file(self, data, filename):
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到: {filepath}")
        except Exception as e:
            print(f"保存文件时出错: {str(e)}")

    def run(self):
        print("开始爬取西南财经大学金融学院网站...")
        
        # 获取主页内容
        main_page = self.get_page_content(self.base_url)
        if main_page:
            print("成功获取页面内容，开始解析...")
            news_data = self.parse_news(main_page)
            
            if news_data:
                # 保存数据
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.save_to_file(news_data, f"swufe_news_{timestamp}.json")
                
                print(f"\n爬取完成，共获取 {len(news_data)} 条新闻")
                print(f"数据已保存到 {self.output_dir} 目录")
            else:
                print("\n未找到任何新闻内容，请检查网站结构是否发生变化")
        else:
            print("获取页面内容失败，请检查网络连接或网站是否可访问")

if __name__ == "__main__":
    spider = SWUFESpider()
    spider.run() 