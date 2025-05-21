# 西南财经大学金融学院网站爬虫

这是一个用于爬取西南财经大学金融学院网站新闻的Python爬虫程序。

## 功能特点

- 自动爬取网站新闻内容
- 保存新闻标题、链接和日期信息
- 数据以JSON格式保存
- 自动创建输出目录

## 环境要求

- Python 3.6+
- 依赖包：见 requirements.txt

## 安装步骤

1. 克隆或下载本项目
2. 安装依赖包：
```bash
pip install -r requirements.txt
```

## 使用方法

直接运行 spider.py 文件：
```bash
python spider.py
```

## 输出说明

- 程序会在当前目录下创建 `output` 文件夹
- 爬取的数据将以JSON格式保存在该文件夹中
- 文件名格式：`swufe_news_YYYYMMDD_HHMMSS.json`

## 注意事项

- 请遵守网站的robots.txt规则
- 建议适当控制爬取频率
- 仅用于学习和研究目的 