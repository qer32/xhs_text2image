// 小红书文生图 - 主JavaScript文件

document.addEventListener('DOMContentLoaded', function() {
    // 初始化Bootstrap提示工具
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // 表单验证
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const textContent = document.getElementById('id_text_content');
            if (textContent && textContent.value.trim() === '') {
                event.preventDefault();
                alert('请输入文本内容！');
                textContent.focus();
            }
        });
    }
    
    // 图片预览放大
    const images = document.querySelectorAll('.image-container img');
    images.forEach(function(img) {
        img.addEventListener('click', function() {
            // 创建模态框
            const modal = document.createElement('div');
            modal.classList.add('modal', 'fade');
            modal.id = 'imageModal';
            modal.setAttribute('tabindex', '-1');
            modal.setAttribute('aria-labelledby', 'imageModalLabel');
            modal.setAttribute('aria-hidden', 'true');
            
            // 模态框内容
            modal.innerHTML = `
                <div class="modal-dialog modal-lg modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="imageModalLabel">图片预览</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${this.src}" class="img-fluid" alt="预览图片">
                        </div>
                        <div class="modal-footer">
                            <a href="${this.src}" download class="btn btn-primary">下载图片</a>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                        </div>
                    </div>
                </div>
            `;
            
            // 添加到文档
            document.body.appendChild(modal);
            
            // 显示模态框
            const modalInstance = new bootstrap.Modal(modal);
            modalInstance.show();
            
            // 模态框关闭后移除
            modal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(modal);
            });
        });
    });
    
    // 背景样式预览
    const backgroundStyleSelect = document.getElementById('id_background_style');
    if (backgroundStyleSelect) {
        const previewContainer = document.createElement('div');
        previewContainer.classList.add('mt-2', 'p-2', 'rounded', 'border');
        previewContainer.style.height = '40px';
        previewContainer.style.backgroundColor = '#fff';
        
        // 添加预览容器到选择框后面
        backgroundStyleSelect.parentNode.appendChild(previewContainer);
        
        // 更新预览
        function updatePreview() {
            const style = backgroundStyleSelect.value;
            
            // 清除之前的样式
            previewContainer.style.backgroundImage = 'none';
            previewContainer.innerHTML = '';
            
            // 设置新样式
            switch(style) {
                case 'plain':
                    previewContainer.style.backgroundColor = '#fff';
                    break;
                case 'notebook':
                    previewContainer.style.backgroundColor = '#fff';
                    previewContainer.style.backgroundImage = 'linear-gradient(#eee 1px, transparent 1px)';
                    previewContainer.style.backgroundSize = '100% 10px';
                    break;
                case 'dot':
                    previewContainer.style.backgroundColor = '#fff';
                    previewContainer.style.backgroundImage = 'radial-gradient(#ccc 1px, transparent 1px)';
                    previewContainer.style.backgroundSize = '10px 10px';
                    break;
                case 'gradient':
                    previewContainer.style.backgroundImage = 'linear-gradient(to bottom, #fff, #f0f0f0)';
                    break;
                case 'paper':
                    previewContainer.style.backgroundColor = '#fffdf9';
                    // 添加一些随机噪点
                    for (let i = 0; i < 20; i++) {
                        const dot = document.createElement('div');
                        dot.style.position = 'absolute';
                        dot.style.width = '1px';
                        dot.style.height = '1px';
                        dot.style.backgroundColor = '#ddd';
                        dot.style.left = Math.random() * 100 + '%';
                        dot.style.top = Math.random() * 100 + '%';
                        previewContainer.appendChild(dot);
                    }
                    break;
            }
        }
        
        // 初始更新
        updatePreview();
        
        // 监听变化
        backgroundStyleSelect.addEventListener('change', updatePreview);
    }
}); 