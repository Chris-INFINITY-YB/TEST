# text_on_image 插件

## 插件功能
本插件基于 silicon API，可将指定文字以自定义参数（大小、颜色、方位、字体、透明度）叠加到底图上，生成新图片。

## 输入参数
- image_url：底图链接（必填）
- text：要添加的文字内容（必填）
- font_size：字体大小（如12，单位px）
- color：文字颜色（如#000000）
- position：文字方位（如left_top/center/right_bottom等）
- font_family：字体类型（如默认/黑体/宋体/楷体等）
- opacity：透明度（0-100）

## 输出参数
- image_url：生成的新图片链接
- summary：生成摘要（可选）

## 使用方法
1. 在 Dify 平台插件管理中注册本插件。
2. 在 Chatflow/Workflow 中添加插件节点，填写参数。
3. 运行后即可获得带文字的新图片链接。

## 依赖
- 需有 silicon api 服务访问权限。
- Python 3.12+
- requests 库



