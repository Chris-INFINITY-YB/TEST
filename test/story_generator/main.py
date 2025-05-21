import os
import requests
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import socket

# 配置 API 密钥
API_KEY = "sk-ctvrdshdqalukolfmzcptppmxlsixdcxcaegqydjnhaytilh"
API_BASE_URL = "https://api.siliconflow.cn/v1"  # 请根据实际的 API 地址修改

class StoryGenerator:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

    def expand_story(self, prompt):
        """根据用户的简单描述扩展故事"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat/completions",
                headers=self.headers,
                json={
                    "model": "deepseek-ai/DeepSeek-R1",  # 请根据实际的模型名称修改
                    "messages": [
                        {"role": "system", "content": "你是一个富有创造力的故事作家。请根据用户的简单描述，扩展成一个完整、有趣的故事。故事应该包含丰富的细节和生动的描述。"},
                        {"role": "user", "content": f"请根据以下描述扩展成一个完整的故事：{prompt}"}
                    ],
                    "max_tokens": 1000
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"故事生成失败：{str(e)}"

    def generate_image(self, story):
        """根据故事生成图像"""
        try:
            # 提取故事的关键场景描述
            response = requests.post(
                f"{API_BASE_URL}/chat/completions",
                headers=self.headers,
                json={
                    "model": "deepseek-ai/DeepSeek-R1",  # 请根据实际的模型名称修改
                    "messages": [
                        {"role": "system", "content": "你是一个图像描述专家。请从故事中提取最具有视觉冲击力的场景，用简洁的英文描述出来。"},
                        {"role": "user", "content": f"请从以下故事中提取最具有视觉冲击力的场景，用简洁的英文描述：{story}"}
                    ],
                    "max_tokens": 100
                }
            )
            response.raise_for_status()
            image_prompt = response.json()["choices"][0]["message"]["content"]

            # 使用图像生成 API
            image_response = requests.post(
                f"{API_BASE_URL}/images/generations",
                headers=self.headers,
                json={
                    "model": "Kwai-Kolors/Kolors",  # 请根据实际的图像模型名称修改
                    "prompt": image_prompt,
                    "size": "1024x1024",
                    "n": 1
                }
            )
            image_response.raise_for_status()
            
            # 下载并保存图像
            image_url = image_response.json()["data"][0]["url"]
            image_data = requests.get(image_url).content
            image = Image.open(BytesIO(image_data))
            image.save("generated_story_image.png")
            
            return "generated_story_image.png"
        except Exception as e:
            return f"图像生成失败：{str(e)}"

def main():
    generator = StoryGenerator()
    
    print("欢迎使用智能故事生成器！")
    print("请输入一个简单的故事描述，我将为您扩展成完整的故事并生成相应的图像。")
    
    while True:
        user_input = input("\n请输入故事描述（输入 'q' 退出）：")
        if user_input.lower() == 'q':
            break
            
        print("\n正在生成故事...")
        story = generator.expand_story(user_input)
        print("\n生成的故事：")
        print("-" * 50)
        print(story)
        print("-" * 50)
        
        print("\n正在生成图像...")
        image_path = generator.generate_image(story)
        if image_path.startswith("图像生成失败"):
            print(image_path)
        else:
            print(f"图像已保存为：{image_path}")

if __name__ == "__main__":
    main() 