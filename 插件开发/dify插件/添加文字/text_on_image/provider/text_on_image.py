from typing import Any
import requests
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class TextOnImageProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            if not credentials.get('api_key'):
                raise ToolProviderCredentialValidationError("API key is required")
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))

    def _get_image_url(self, parameters: dict[str, Any]) -> str:
        # 尝试从不同位置获取图片URL
        image_url = parameters.get('image_url', '')
        
        # 如果image_url为空，尝试从files数组中获取
        if not image_url and 'files' in parameters:
            files = parameters['files']
            if isinstance(files, list) and len(files) > 0:
                file_info = files[0]
                if isinstance(file_info, dict):
                    # 优先使用remote_url
                    image_url = file_info.get('remote_url', '')
                    if not image_url:
                        # 如果没有remote_url，尝试使用url
                        image_url = file_info.get('url', '')
                    if not image_url and 'data' in file_info:
                        # 如果是Flux插件的输出格式，从data中获取url
                        data = file_info.get('data', [])
                        if isinstance(data, list) and len(data) > 0:
                            image_url = data[0].get('url', '')
        
        return image_url

    def _invoke(self, credentials: dict[str, Any], parameters: dict[str, Any]) -> dict[str, Any]:
        try:
            api_key = credentials.get('api_key')
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            # 获取图片URL
            image_url = self._get_image_url(parameters)
            if not image_url:
                return {
                    'text': '',
                    'files': [],
                    'json': [{'error': 'No valid image URL found in the input parameters'}]
                }
            
            # 构建SiliconFlow API请求
            payload = {
                'prompt': f"Add text '{parameters.get('text')}' to the image with font size {parameters.get('font_size')}, color {parameters.get('color')}, position {parameters.get('position')}, font family {parameters.get('font_family')}, and opacity {parameters.get('opacity')}%",
                'image_url': image_url,
                'negative_prompt': '',
                'model': 'flux',
                'steps': 20,
                'width': 1024,
                'height': 1024,
                'seed': -1,
                'cfg_scale': 7.5,
                'sampler': 'DPM++ 2M Karras'
            }
            
            # 使用SiliconFlow的Flux API端点
            response = requests.post(
                'https://api.siliconflow.cn/v1/flux/generate',
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                return {
                    'text': '',
                    'files': [],
                    'json': [{'error': f'{response.status_code} {response.reason}: {response.text}'}]
                }
            
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                image_url = result['data'][0].get('url', '')
                return {
                    'text': 'Successfully added text to image',
                    'files': [{
                        'type': 'image',
                        'transfer_method': 'tool_file',
                        'remote_url': image_url,
                        'mime_type': 'image/jpeg'
                    }],
                    'json': [result]
                }
            else:
                return {
                    'text': '',
                    'files': [],
                    'json': [{'error': 'No image URL in response'}]
                }
            
        except Exception as e:
            return {
                'text': '',
                'files': [],
                'json': [{'error': str(e)}]
            }
