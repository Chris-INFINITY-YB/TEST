from collections.abc import Generator
from typing import Any
import requests
import os
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

SILICON_API_KEY = "sk-ctvrdshdqalukolfmzcptppmxlsixdcxcaegqydjnhaytilh"
SILICON_API_BASE_URL = "https://api.siliconflow.cn/v1"

class TextOnImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 参数提取
        image_url = tool_parameters.get("image_url")
        text = tool_parameters.get("text")
        font_size = tool_parameters.get("font_size")
        color = tool_parameters.get("color")
        position = tool_parameters.get("position")
        font_family = tool_parameters.get("font_family")
        opacity = tool_parameters.get("opacity")

        # 参数校验
        for k, v in zip([
            "image_url", "text", "font_size", "color", "position", "font_family", "opacity"
        ], [image_url, text, font_size, color, position, font_family, opacity]):
            if v is None:
                yield self.create_json_message({"error": f"Missing parameter: {k}"})
                return

        payload = {
            "image_url": image_url,
            "text": text,
            "font_size": font_size,
            "color": color,
            "position": position,
            "font_family": font_family,
            "opacity": opacity
        }
        headers = {
            "Authorization": f"Bearer {SILICON_API_KEY}",
            "Content-Type": "application/json"
        }
        try:
            resp = requests.post(
                f"{SILICON_API_BASE_URL}/image/text/add",
                headers=headers,
                json=payload,
                timeout=30
            )
            resp.raise_for_status()
            data = resp.json()
            yield self.create_json_message({
                "image_url": data.get("image_url", ""),
                "summary": data.get("summary", "")
            })
        except Exception as e:
            yield self.create_json_message({"error": str(e)})
