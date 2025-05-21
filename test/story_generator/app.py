from flask import Flask, render_template, request, jsonify, send_file
from main import StoryGenerator
import os
from datetime import datetime

# 获取当前文件所在目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
           static_folder=os.path.join(BASE_DIR, 'static'),
           template_folder=os.path.join(BASE_DIR, 'templates'))
app.config['SECRET_KEY'] = os.urandom(24)
generator = StoryGenerator()

@app.route('/test')
def test():
    return "Flask 服务器正在运行！"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        prompt = request.json.get('prompt', '')
        if not prompt:
            return jsonify({'error': '请输入故事描述'}), 400

        # 生成故事
        story = generator.expand_story(prompt)
        if story.startswith('故事生成失败'):
            return jsonify({'error': story}), 500

        # 生成图像
        image_path = generator.generate_image(story)
        if image_path.startswith('图像生成失败'):
            return jsonify({'error': image_path}), 500

        # 生成唯一的文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_image_path = f'static/images/story_{timestamp}.png'
        
        # 确保目录存在
        os.makedirs(os.path.join(BASE_DIR, 'static/images'), exist_ok=True)
        
        # 移动图像到静态目录
        os.rename(image_path, os.path.join(BASE_DIR, new_image_path))

        return jsonify({
            'story': story,
            'image_url': f'/{new_image_path}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 