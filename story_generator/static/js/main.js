document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const promptInput = document.getElementById('prompt');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const storyDiv = document.getElementById('story');
    const storyImage = document.getElementById('storyImage');
    const errorDiv = document.getElementById('error');

    generateBtn.addEventListener('click', async function() {
        const prompt = promptInput.value.trim();
        
        if (!prompt) {
            showError('请输入故事描述');
            return;
        }

        // 重置界面
        hideError();
        hideResult();
        showLoading();

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || '生成失败，请稍后重试');
            }

            // 显示结果
            storyDiv.textContent = data.story;
            storyImage.src = data.image_url;
            showResult();

        } catch (error) {
            showError(error.message);
        } finally {
            hideLoading();
        }
    });

    function showLoading() {
        loadingDiv.classList.remove('hidden');
        generateBtn.disabled = true;
    }

    function hideLoading() {
        loadingDiv.classList.add('hidden');
        generateBtn.disabled = false;
    }

    function showResult() {
        resultDiv.classList.remove('hidden');
    }

    function hideResult() {
        resultDiv.classList.add('hidden');
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    function hideError() {
        errorDiv.classList.add('hidden');
    }
}); 