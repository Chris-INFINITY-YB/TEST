import requests
from typing import Dict

# Silicon API配置（请根据实际情况填写）
SILICON_API_KEY = "sk-ctvrdshdqalukolfmzcptppmxlsixdcxcaegqydjnhaytilh"
SILICON_API_BASE_URL = "https://api.siliconflow.cn/v1"

# Dify插件主入口
class SiliconTextOnImagePlugin:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {SILICON_API_KEY}",
            "Content-Type": "application/json"
        }

    def add_text_to_image(self, params: Dict) -> Dict:
        """
        params: {
            'image_url': str,  # 底图链接
            'text': str,       # 文字内容
            'font_size': int,  # 字体大小
            'color': str,      # 文字颜色（如#000000）
            'position': str,   # 方位（如'left_top'/'center'等）
            'font_family': str,# 字体类型
            'opacity': int     # 透明度（0-100）
        }
        """
        # 参数校验
        required = ['image_url', 'text', 'font_size', 'color', 'position', 'font_family', 'opacity']
        for key in required:
            if key not in params:
                return {"error": f"缺少参数: {key}"}

        # 构造API请求体
        payload = {
            "image_url": params['image_url'],
            "text": params['text'],
            "font_size": params['font_size'],
            "color": params['color'],
            "position": params['position'],
            "font_family": params['font_family'],
            "opacity": params['opacity']
        }
        try:
            resp = requests.post(
                f"{SILICON_API_BASE_URL}/image/text/add",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "image_url": data.get("image_url", ""),
                "summary": data.get("summary", "")
            }
        except Exception as e:
            return {"error": str(e)}

# Dify插件接口示例（可根据实际Dify插件开发脚手架调整）
def plugin_entry(inputs: Dict) -> Dict:
    """
    Dify插件标准入口
    inputs: {
        'image_url': str,
        'text': str,
        'font_size': int,
        'color': str,
        'position': str,
        'font_family': str,
        'opacity': int,
        'user_agent': str,
        'generate_summary': bool
    }
    """
    plugin = SiliconTextOnImagePlugin()
    result = plugin.add_text_to_image(inputs)
    return result 