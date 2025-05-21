# Dify插件：底图文字生成器

## 插件功能
本插件可将指定文字以自定义参数（大小、颜色、方位、字体、透明度）叠加到底图上，生成新图片。所有图像处理均通过silicon api实现。

## 输入参数
- image_url：底图链接（必填）
- text：要添加的文字内容（必填）
- font_size：字体大小（如12，单位px）
- color：文字颜色（如#000000）
- position：文字方位（如left_top/center/right_bottom等）
- font_family：字体类型（如默认/黑体/宋体/楷体等）
- opacity：透明度（0-100）
- user_agent：用户代理（可选）
- generate_summary：是否生成摘要（可选）

## 输出参数
- image_url：生成的新图片链接
- summary：生成摘要（可选）

## 使用方法
1. 配置silicon api密钥和地址。
2. 按Dify插件开发规范部署本插件。
3. 通过Dify平台UI或API传入参数，获取生成图片链接。

## 依赖
- 需有silicon api服务访问权限。
- Python 3.8+
- requests库

## 目录结构
- silicon_text_on_image_plugin.py 插件主代码
- 插件需求、UI示意图、README.md 说明文档 