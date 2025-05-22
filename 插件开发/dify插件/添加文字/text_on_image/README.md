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

## 更新日志

### 2024-03-21
- 会话主要目的：修复插件运行时404错误问题
- 完成的主要任务：
  - 完善了插件代码实现
  - 添加了API调用逻辑
  - 添加了错误处理机制
- 关键决策和解决方案：
  - 实现了完整的API调用逻辑
  - 添加了请求头和认证机制
  - 完善了错误处理和响应处理
- 使用的技术栈：
  - Python
  - requests库
  - Dify Plugin SDK
- 修改的文件：
  - provider/text_on_image.py
  - requirements.txt

### 2024-03-21 (第二次更新)
- 会话主要目的：修复图片URL获取问题
- 完成的主要任务：
  - 添加了图片URL提取逻辑
  - 支持从files数组中获取图片URL
  - 增加了URL验证和错误处理
- 关键决策和解决方案：
  - 实现了`_get_image_url`方法处理多种URL来源
  - 优先使用remote_url，其次使用url字段
  - 添加了URL有效性检查
- 使用的技术栈：
  - Python
  - requests库
  - Dify Plugin SDK
- 修改的文件：
  - provider/text_on_image.py

### 2024-03-21 (第三次更新)
- 会话主要目的：修复SiliconFlow API调用问题
- 完成的主要任务：
  - 更新了API端点为Flux API
  - 修改了请求参数格式
  - 优化了响应处理逻辑
- 关键决策和解决方案：
  - 使用SiliconFlow的Flux API替代原有的text/add API
  - 将文字参数转换为Flux API所需的prompt格式
  - 添加了更多的图像生成参数
- 使用的技术栈：
  - Python
  - requests库
  - Dify Plugin SDK
  - SiliconFlow Flux API
- 修改的文件：
  - provider/text_on_image.py

### 2024-03-21 (第四次更新)
- 会话主要目的：优化Flux插件文件处理
- 完成的主要任务：
  - 增加了对Flux插件输出格式的支持
  - 优化了文件URL提取逻辑
  - 规范化了输出文件格式
- 关键决策和解决方案：
  - 添加了对Flux插件data字段的处理
  - 统一了文件输出格式为Dify标准格式
  - 增加了更多的文件类型信息
- 使用的技术栈：
  - Python
  - requests库
  - Dify Plugin SDK
  - SiliconFlow Flux API
- 修改的文件：
  - provider/text_on_image.py

## 本地部署说明

### 构建插件
1. 在插件目录下执行：
   ```bash
   python -m pip install build
   python -m build
   ```
   这将在`dist`目录下生成插件包文件。

### 导入插件到Dify
1. 复制插件包
   - 将`dist`目录下的`.whl`文件复制到Dify的插件目录
   - Docker部署：`/path/to/dify/plugins/`
   - 源码部署：`/path/to/dify/backend/plugins/`

2. 在Dify中导入
   - 登录Dify管理后台
   - 进入"插件管理"页面
   - 点击"导入插件"
   - 选择插件包文件

3. 配置插件
   - 在插件管理页面找到"text_on_image"插件
   - 点击"配置"
   - 填写SiliconFlow API密钥

4. 重启服务
   - Docker部署：
     ```bash
     docker-compose restart
     ```
   - 源码部署：
     ```bash
     cd /path/to/dify/backend
     python app.py
     ```

5. 测试插件
   - 在Chatflow/Workflow中添加插件节点
   - 配置参数并测试



