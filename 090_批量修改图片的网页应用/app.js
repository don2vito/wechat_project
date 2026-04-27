/**
 * 批量图片修改工具 - 主应用逻辑
 */

// ========================================
// 全局状态管理
// ========================================
const AppState = {
    images: [], // 存储所有图片数据
    selectedIds: new Set(), // 选中的图片ID
    currentFilter: 'none', // 当前滤镜
    history: [], // 操作历史
    historyIndex: -1, // 当前历史位置
    maxHistory: 10, // 最大历史记录数
    isProcessing: false // 是否正在处理
};

// 图片数据类
class ImageItem {
    constructor(file, id) {
        this.id = id;
        this.file = file;
        this.originalName = file.name;
        this.displayName = file.name;
        this.size = file.size;
        this.type = file.type;
        this.url = null;
        this.thumbnailUrl = null;
        this.originalImage = null; // 原始图片对象
        
        // 调整参数
        this.adjustments = {
            brightness: 50,      // 0-100
            saturation: 0,       // -100 to 100
            contrast: 50,        // 0-100
            hue: 0,              // 0-360
            filter: 'none'
        };
    }
}

// ========================================
// DOM 元素引用
// ========================================
const DOM = {
    // 上传相关
    dropZone: document.getElementById('dropZone'),
    fileInput: document.getElementById('fileInput'),
    uploadBtn: document.getElementById('uploadBtn'),
    
    // 预览相关
    imageGrid: document.getElementById('imageGrid'),
    imageCount: document.getElementById('imageCount'),
    selectAllBtn: document.getElementById('selectAllBtn'),
    deselectAllBtn: document.getElementById('deselectAllBtn'),
    deleteSelectedBtn: document.getElementById('deleteSelectedBtn'),
    
    // 调整参数
    brightness: document.getElementById('brightness'),
    brightnessValue: document.getElementById('brightnessValue'),
    saturation: document.getElementById('saturation'),
    saturationValue: document.getElementById('saturationValue'),
    contrast: document.getElementById('contrast'),
    contrastValue: document.getElementById('contrastValue'),
    hue: document.getElementById('hue'),
    hueValue: document.getElementById('hueValue'),
    applyToAllBtn: document.getElementById('applyToAllBtn'),
    
    // 滤镜
    filterBtns: document.querySelectorAll('.filter-btn'),
    
    // 重命名
    baseName: document.getElementById('baseName'),
    startNumber: document.getElementById('startNumber'),
    numberDigits: document.getElementById('numberDigits'),
    renamePreview: document.getElementById('renamePreview'),
    applyRenameBtn: document.getElementById('applyRenameBtn'),
    
    // 导出设置
    compression: document.getElementById('compression'),
    outputSize: document.getElementById('outputSize'),
    customSizeGroup: document.getElementById('customSizeGroup'),
    customWidth: document.getElementById('customWidth'),
    customHeight: document.getElementById('customHeight'),
    useWorker: document.getElementById('useWorker'),
    
    // 底部操作
    downloadBtn: document.getElementById('downloadBtn'),
    progressContainer: document.getElementById('progressContainer'),
    progressText: document.getElementById('progressText'),
    progressPercent: document.getElementById('progressPercent'),
    progressFill: document.getElementById('progressFill'),
    progressDetail: document.getElementById('progressDetail'),
    
    // 撤销/重做
    undoBtn: document.getElementById('undoBtn'),
    redoBtn: document.getElementById('redoBtn'),
    resetAllBtn: document.getElementById('resetAllBtn'),
    
    // 模态框
    previewModal: document.getElementById('previewModal'),
    previewImage: document.getElementById('previewImage'),
    previewFileName: document.getElementById('previewFileName'),
    previewFileSize: document.getElementById('previewFileSize'),
    closeBtn: document.querySelector('.close-btn'),
    
    // 提示
    toastContainer: document.getElementById('toastContainer')
};

// ========================================
// 工具函数
// ========================================

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 生成唯一ID
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// 显示提示消息
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    DOM.toastContainer.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, duration);
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ========================================
// 图片处理函数
// ========================================

// 读取文件为DataURL
function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (e) => reject(e);
        reader.readAsDataURL(file);
    });
}

// 加载图片
function loadImage(src) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => resolve(img);
        img.onerror = (e) => reject(e);
        img.src = src;
    });
}

// 生成缩略图
async function generateThumbnail(imageUrl, maxSize = 150) {
    const img = await loadImage(imageUrl);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // 计算缩放比例
    const scale = Math.min(maxSize / img.width, maxSize / img.height);
    canvas.width = img.width * scale;
    canvas.height = img.height * scale;
    
    // 绘制图片
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    
    return canvas.toDataURL('image/jpeg', 0.8);
}

// 应用滤镜和调整
function applyFilters(ctx, width, height, adjustments) {
    const { brightness, saturation, contrast, hue, filter } = adjustments;
    
    // 创建临时canvas
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = width;
    tempCanvas.height = height;
    const tempCtx = tempCanvas.getContext('2d');
    
    // 获取图像数据
    const imageData = ctx.getImageData(0, 0, width, height);
    const data = imageData.data;
    
    // 应用滤镜
    for (let i = 0; i < data.length; i += 4) {
        let r = data[i];
        let g = data[i + 1];
        let b = data[i + 2];
        
        // 应用预设滤镜
        switch (filter) {
            case 'grayscale':
                const gray = r * 0.299 + g * 0.587 + b * 0.114;
                r = g = b = gray;
                break;
            case 'vintage':
                // 棕褐色调
                const tr = r * 0.393 + g * 0.769 + b * 0.189;
                const tg = r * 0.349 + g * 0.686 + b * 0.168;
                const tb = r * 0.272 + g * 0.534 + b * 0.131;
                r = tr;
                g = tg;
                b = tb;
                break;
            case 'vivid':
                // 增加饱和度（在HSL调整中处理）
                break;
            case 'cool':
                r *= 0.9;
                b *= 1.1;
                break;
            case 'warm':
                r *= 1.1;
                b *= 0.9;
                break;
        }
        
        // 应用亮度调整 (50%为基准)
        const brightnessFactor = (brightness - 50) / 50;
        r += r * brightnessFactor;
        g += g * brightnessFactor;
        b += b * brightnessFactor;
        
        // 应用对比度调整 (50%为基准)
        const contrastFactor = (contrast - 50) / 50;
        r = ((r - 128) * (1 + contrastFactor)) + 128;
        g = ((g - 128) * (1 + contrastFactor)) + 128;
        b = ((b - 128) * (1 + contrastFactor)) + 128;
        
        // 应用饱和度调整
        if (saturation !== 0 || filter === 'vivid') {
            const satFactor = 1 + (saturation / 100) + (filter === 'vivid' ? 0.3 : 0);
            const luminance = r * 0.299 + g * 0.587 + b * 0.114;
            r = luminance + (r - luminance) * satFactor;
            g = luminance + (g - luminance) * satFactor;
            b = luminance + (b - luminance) * satFactor;
        }
        
        // 限制值范围
        data[i] = Math.max(0, Math.min(255, r));
        data[i + 1] = Math.max(0, Math.min(255, g));
        data[i + 2] = Math.max(0, Math.min(255, b));
    }
    
    // 应用色相旋转（使用canvas滤镜）
    if (hue !== 0) {
        tempCtx.filter = `hue-rotate(${hue}deg)`;
    }
    
    tempCtx.putImageData(imageData, 0, 0);
    
    // 如果有色相调整，需要再绘制一次
    if (hue !== 0) {
        ctx.filter = `hue-rotate(${hue}deg)`;
        ctx.drawImage(tempCanvas, 0, 0);
        ctx.filter = 'none';
    } else {
        ctx.drawImage(tempCanvas, 0, 0);
    }
}

// 处理单张图片
async function processImage(imageItem, quality = 0.9, maxWidth = null, maxHeight = null) {
    const img = await loadImage(imageItem.url);
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // 计算输出尺寸
    let width = img.width;
    let height = img.height;
    
    if (maxWidth && width > maxWidth) {
        height = (height * maxWidth) / width;
        width = maxWidth;
    }
    if (maxHeight && height > maxHeight) {
        width = (width * maxHeight) / height;
        height = maxHeight;
    }
    
    canvas.width = width;
    canvas.height = height;
    
    // 绘制原图
    ctx.drawImage(img, 0, 0, width, height);
    
    // 应用滤镜和调整
    applyFilters(ctx, width, height, imageItem.adjustments);
    
    // 导出
    const mimeType = imageItem.type === 'image/png' ? 'image/png' : 'image/jpeg';
    return canvas.toDataURL(mimeType, quality);
}

// ========================================
// 历史记录管理
// ========================================

// 保存状态到历史
function saveState() {
    // 删除当前位置之后的历史
    AppState.history = AppState.history.slice(0, AppState.historyIndex + 1);
    
    // 保存当前状态
    const state = {
        images: AppState.images.map(img => ({
            id: img.id,
            displayName: img.displayName,
            adjustments: { ...img.adjustments }
        })),
        selectedIds: Array.from(AppState.selectedIds)
    };
    
    AppState.history.push(state);
    
    // 限制历史记录数量
    if (AppState.history.length > AppState.maxHistory) {
        AppState.history.shift();
    } else {
        AppState.historyIndex++;
    }
    
    updateUndoRedoButtons();
}

// 撤销
function undo() {
    if (AppState.historyIndex > 0) {
        AppState.historyIndex--;
        restoreState(AppState.history[AppState.historyIndex]);
        showToast('已撤销', 'info');
    }
}

// 重做
function redo() {
    if (AppState.historyIndex < AppState.history.length - 1) {
        AppState.historyIndex++;
        restoreState(AppState.history[AppState.historyIndex]);
        showToast('已重做', 'info');
    }
}

// 恢复状态
function restoreState(state) {
    // 恢复图片调整参数
    state.images.forEach(savedImg => {
        const img = AppState.images.find(i => i.id === savedImg.id);
        if (img) {
            img.displayName = savedImg.displayName;
            img.adjustments = { ...savedImg.adjustments };
        }
    });
    
    // 恢复选中状态
    AppState.selectedIds = new Set(state.selectedIds);
    
    // 更新UI
    updateImageGrid();
    updateControlsFromSelection();
    updateUndoRedoButtons();
}

// 更新撤销/重做按钮状态
function updateUndoRedoButtons() {
    DOM.undoBtn.disabled = AppState.historyIndex <= 0;
    DOM.redoBtn.disabled = AppState.historyIndex >= AppState.history.length - 1;
}

// ========================================
// UI 更新函数
// ========================================

// 更新图片网格
function updateImageGrid() {
    if (AppState.images.length === 0) {
        DOM.imageGrid.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">🖼️</span>
                <p>暂无图片</p>
                <p class="hint">请导入图片开始编辑</p>
            </div>
        `;
        DOM.imageCount.textContent = '(0张)';
        DOM.downloadBtn.disabled = true;
        return;
    }
    
    DOM.imageGrid.innerHTML = '';
    AppState.images.forEach((image, index) => {
        const card = createImageCard(image, index);
        DOM.imageGrid.appendChild(card);
    });
    
    DOM.imageCount.textContent = `(${AppState.images.length}张)`;
    DOM.downloadBtn.disabled = false;
}

// 创建图片卡片
function createImageCard(imageItem, index) {
    const card = document.createElement('div');
    card.className = `image-card ${AppState.selectedIds.has(imageItem.id) ? 'selected' : ''}`;
    card.dataset.id = imageItem.id;
    
    const isSelected = AppState.selectedIds.has(imageItem.id);
    const selectionOrder = isSelected ? Array.from(AppState.selectedIds).indexOf(imageItem.id) + 1 : 0;
    
    card.innerHTML = `
        <img class="thumbnail" src="${imageItem.thumbnailUrl}" alt="${imageItem.displayName}">
        <div class="image-info">
            <div class="image-name" title="${imageItem.displayName}">${imageItem.displayName}</div>
            <div class="image-size">${formatFileSize(imageItem.size)}</div>
        </div>
        <div class="image-actions">
            <button class="action-btn" title="预览" onclick="event.stopPropagation(); previewImage('${imageItem.id}')">👁</button>
            <button class="action-btn" title="删除" onclick="event.stopPropagation(); deleteImage('${imageItem.id}')">🗑</button>
        </div>
        ${isSelected ? `<div class="selection-indicator">${selectionOrder}</div>` : ''}
    `;
    
    // 点击选中/取消选中
    card.addEventListener('click', (e) => {
        if (e.ctrlKey || e.metaKey) {
            // Ctrl+点击：多选
            toggleSelection(imageItem.id);
        } else {
            // 普通点击：单选
            AppState.selectedIds.clear();
            AppState.selectedIds.add(imageItem.id);
            updateImageGrid();
            updateControlsFromSelection();
        }
    });
    
    return card;
}

// 切换选中状态
function toggleSelection(id) {
    if (AppState.selectedIds.has(id)) {
        AppState.selectedIds.delete(id);
    } else {
        AppState.selectedIds.add(id);
    }
    updateImageGrid();
    updateControlsFromSelection();
}

// 从选中项更新控制面板
function updateControlsFromSelection() {
    const selectedImages = AppState.images.filter(img => AppState.selectedIds.has(img.id));
    
    if (selectedImages.length === 0) {
        // 没有选中，使用默认值
        DOM.brightness.value = 50;
        DOM.brightnessValue.textContent = '50%';
        DOM.saturation.value = 0;
        DOM.saturationValue.textContent = '0%';
        DOM.contrast.value = 50;
        DOM.contrastValue.textContent = '50%';
        DOM.hue.value = 0;
        DOM.hueValue.textContent = '0°';
        
        // 重置滤镜按钮
        DOM.filterBtns.forEach(btn => btn.classList.remove('active'));
        DOM.filterBtns[0].classList.add('active');
        return;
    }
    
    // 使用第一个选中项的参数
    const firstImage = selectedImages[0];
    DOM.brightness.value = firstImage.adjustments.brightness;
    DOM.brightnessValue.textContent = firstImage.adjustments.brightness + '%';
    DOM.saturation.value = firstImage.adjustments.saturation;
    DOM.saturationValue.textContent = firstImage.adjustments.saturation + '%';
    DOM.contrast.value = firstImage.adjustments.contrast;
    DOM.contrastValue.textContent = firstImage.adjustments.contrast + '%';
    DOM.hue.value = firstImage.adjustments.hue;
    DOM.hueValue.textContent = firstImage.adjustments.hue + '°';
    
    // 更新滤镜按钮
    DOM.filterBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === firstImage.adjustments.filter);
    });
}

// 更新选中图片的调整参数
function updateSelectedAdjustments(adjustmentType, value) {
    const selectedImages = AppState.images.filter(img => AppState.selectedIds.has(img.id));
    
    selectedImages.forEach(image => {
        image.adjustments[adjustmentType] = value;
    });
    
    // 更新缩略图预览
    updateThumbnailsForSelected();
}

// 更新选中图片的缩略图
async function updateThumbnailsForSelected() {
    const selectedImages = AppState.images.filter(img => AppState.selectedIds.has(img.id));
    
    for (const image of selectedImages) {
        // 重新生成带滤镜的缩略图
        try {
            const processedUrl = await processImage(image, 0.8, 150);
            image.thumbnailUrl = processedUrl;
        } catch (e) {
            console.error('更新缩略图失败:', e);
        }
    }
    
    updateImageGrid();
}

// ========================================
// 文件导入处理
// ========================================

// 处理文件导入
async function handleFiles(files) {
    const validFiles = Array.from(files).filter(file => {
        // 验证格式
        if (!file.type.match(/image\/(jpeg|png)/)) {
            showToast(`跳过不支持的格式: ${file.name}`, 'warning');
            return false;
        }
        
        // 验证大小
        if (file.size > 10 * 1024 * 1024) {
            showToast(`警告: ${file.name} 超过10MB，处理可能较慢`, 'warning');
        }
        
        return true;
    });
    
    if (validFiles.length === 0) return;
    
    // 检查总数限制
    if (AppState.images.length + validFiles.length > 20) {
        showToast('单次处理建议不超过20张图片', 'warning');
    }
    
    showToast(`正在导入 ${validFiles.length} 张图片...`, 'info');
    
    for (const file of validFiles) {
        try {
            const id = generateId();
            const imageItem = new ImageItem(file, id);
            
            // 读取文件
            const dataUrl = await readFileAsDataURL(file);
            imageItem.url = dataUrl;
            
            // 生成缩略图
            const thumbnailUrl = await generateThumbnail(dataUrl, 150);
            imageItem.thumbnailUrl = thumbnailUrl;
            
            // 加载原图
            imageItem.originalImage = await loadImage(dataUrl);
            
            AppState.images.push(imageItem);
        } catch (e) {
            console.error('导入图片失败:', e);
            showToast(`导入失败: ${file.name}`, 'error');
        }
    }
    
    updateImageGrid();
    saveState();
    showToast(`成功导入 ${validFiles.length} 张图片`, 'success');
}

// ========================================
// 图片操作
// ========================================

// 预览图片
function previewImage(id) {
    const image = AppState.images.find(img => img.id === id);
    if (!image) return;
    
    DOM.previewImage.src = image.url;
    DOM.previewFileName.textContent = image.displayName;
    DOM.previewFileSize.textContent = formatFileSize(image.size);
    DOM.previewModal.classList.add('active');
}

// 删除单张图片
function deleteImage(id) {
    const index = AppState.images.findIndex(img => img.id === id);
    if (index === -1) return;
    
    AppState.images.splice(index, 1);
    AppState.selectedIds.delete(id);
    
    updateImageGrid();
    updateControlsFromSelection();
    saveState();
    showToast('图片已删除', 'info');
}

// 删除选中的图片
function deleteSelectedImages() {
    if (AppState.selectedIds.size === 0) {
        showToast('请先选择要删除的图片', 'warning');
        return;
    }
    
    AppState.images = AppState.images.filter(img => !AppState.selectedIds.has(img.id));
    AppState.selectedIds.clear();
    
    updateImageGrid();
    updateControlsFromSelection();
    saveState();
    showToast('选中图片已删除', 'info');
}

// ========================================
// 重命名功能
// ========================================

// 更新重命名预览
function updateRenamePreview() {
    const baseName = DOM.baseName.value.trim() || 'image';
    const startNum = parseInt(DOM.startNumber.value) || 1;
    const digits = parseInt(DOM.numberDigits.value) || 3;
    
    const numStr = startNum.toString().padStart(digits, '0');
    DOM.renamePreview.textContent = `${baseName}_${numStr}.jpg`;
}

// 应用重命名
function applyRename() {
    if (AppState.images.length === 0) {
        showToast('没有可重命名的图片', 'warning');
        return;
    }
    
    const baseName = DOM.baseName.value.trim();
    if (!baseName) {
        showToast('请输入基础名称', 'warning');
        return;
    }
    
    const startNum = parseInt(DOM.startNumber.value) || 1;
    const digits = parseInt(DOM.numberDigits.value) || 3;
    
    AppState.images.forEach((image, index) => {
        const num = (startNum + index).toString().padStart(digits, '0');
        const ext = image.type === 'image/png' ? 'png' : 'jpg';
        image.displayName = `${baseName}_${num}.${ext}`;
    });
    
    updateImageGrid();
    saveState();
    showToast('重命名完成', 'success');
}

// ========================================
// 导出功能
// ========================================

// 导出图片
async function exportImages() {
    if (AppState.images.length === 0) {
        showToast('没有可导出的图片', 'warning');
        return;
    }
    
    if (AppState.isProcessing) {
        showToast('正在处理中，请稍候...', 'warning');
        return;
    }
    
    AppState.isProcessing = true;
    DOM.progressContainer.style.display = 'block';
    DOM.downloadBtn.disabled = true;
    
    const quality = parseFloat(DOM.compression.value);
    const outputSize = DOM.outputSize.value;
    const useWorker = DOM.useWorker.checked;
    
    let maxWidth = null;
    let maxHeight = null;
    
    if (outputSize === 'custom') {
        maxWidth = parseInt(DOM.customWidth.value) || null;
        maxHeight = parseInt(DOM.customHeight.value) || null;
    } else if (outputSize !== 'original') {
        maxWidth = parseInt(outputSize);
    }
    
    const zip = new JSZip();
    const total = AppState.images.length;
    
    try {
        for (let i = 0; i < AppState.images.length; i++) {
            const image = AppState.images[i];
            
            // 更新进度
            const progress = Math.round((i / total) * 100);
            DOM.progressFill.style.width = progress + '%';
            DOM.progressPercent.textContent = progress + '%';
            DOM.progressDetail.textContent = `${i + 1}/${total}`;
            DOM.progressText.textContent = `正在处理: ${image.displayName}`;
            
            // 处理图片
            const processedDataUrl = await processImage(image, quality, maxWidth, maxHeight);
            
            // 转换为blob
            const response = await fetch(processedDataUrl);
            const blob = await response.blob();
            
            // 添加到zip
            zip.file(image.displayName, blob);
            
            // 小延迟让UI更新
            await new Promise(resolve => setTimeout(resolve, 10));
        }
        
        // 完成
        DOM.progressFill.style.width = '100%';
        DOM.progressPercent.textContent = '100%';
        DOM.progressText.textContent = '正在打包...';
        
        // 生成zip
        const zipBlob = await zip.generateAsync({ type: 'blob' });
        
        // 下载
        const zipName = `processed_images_${Date.now()}.zip`;
        saveAs(zipBlob, zipName);
        
        showToast('导出成功！', 'success');
    } catch (e) {
        console.error('导出失败:', e);
        showToast('导出失败: ' + e.message, 'error');
    } finally {
        AppState.isProcessing = false;
        DOM.progressContainer.style.display = 'none';
        DOM.downloadBtn.disabled = false;
        DOM.progressFill.style.width = '0%';
    }
}

// ========================================
// 重置功能
// ========================================

// 重置选中图片
function resetSelected() {
    const selectedImages = AppState.images.filter(img => AppState.selectedIds.has(img.id));
    
    if (selectedImages.length === 0) {
        showToast('请先选择要重置的图片', 'warning');
        return;
    }
    
    selectedImages.forEach(image => {
        image.adjustments = {
            brightness: 50,
            saturation: 0,
            contrast: 50,
            hue: 0,
            filter: 'none'
        };
    });
    
    updateControlsFromSelection();
    updateThumbnailsForSelected();
    saveState();
    showToast('已重置选中图片', 'info');
}

// 重置全部
function resetAll() {
    if (AppState.images.length === 0) return;
    
    if (!confirm('确定要重置所有图片的调整参数吗？')) return;
    
    AppState.images.forEach(image => {
        image.adjustments = {
            brightness: 50,
            saturation: 0,
            contrast: 50,
            hue: 0,
            filter: 'none'
        };
    });
    
    AppState.selectedIds.clear();
    updateControlsFromSelection();
    updateImageGrid();
    saveState();
    showToast('已重置所有图片', 'info');
}

// ========================================
// 事件绑定
// ========================================

// 初始化
function init() {
    // 上传按钮点击
    DOM.uploadBtn.addEventListener('click', () => DOM.fileInput.click());
    
    // 文件选择
    DOM.fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
        DOM.fileInput.value = ''; // 重置以便可以重复选择相同文件
    });
    
    // 拖曳上传
    DOM.dropZone.addEventListener('click', () => DOM.fileInput.click());
    
    DOM.dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        DOM.dropZone.classList.add('dragover');
    });
    
    DOM.dropZone.addEventListener('dragleave', () => {
        DOM.dropZone.classList.remove('dragover');
    });
    
    DOM.dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        DOM.dropZone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });
    
    // 调整参数滑块
    const debouncedUpdate = debounce(() => {
        updateThumbnailsForSelected();
        saveState();
    }, 300);
    
    DOM.brightness.addEventListener('input', (e) => {
        DOM.brightnessValue.textContent = e.target.value + '%';
        updateSelectedAdjustments('brightness', parseInt(e.target.value));
        debouncedUpdate();
    });
    
    DOM.saturation.addEventListener('input', (e) => {
        DOM.saturationValue.textContent = e.target.value + '%';
        updateSelectedAdjustments('saturation', parseInt(e.target.value));
        debouncedUpdate();
    });
    
    DOM.contrast.addEventListener('input', (e) => {
        DOM.contrastValue.textContent = e.target.value + '%';
        updateSelectedAdjustments('contrast', parseInt(e.target.value));
        debouncedUpdate();
    });
    
    DOM.hue.addEventListener('input', (e) => {
        DOM.hueValue.textContent = e.target.value + '°';
        updateSelectedAdjustments('hue', parseInt(e.target.value));
        debouncedUpdate();
    });
    
    // 应用到全部
    DOM.applyToAllBtn.addEventListener('click', () => {
        if (AppState.images.length === 0) {
            showToast('没有可应用的图片', 'warning');
            return;
        }
        
        const adjustments = {
            brightness: parseInt(DOM.brightness.value),
            saturation: parseInt(DOM.saturation.value),
            contrast: parseInt(DOM.contrast.value),
            hue: parseInt(DOM.hue.value),
            filter: AppState.currentFilter
        };
        
        AppState.images.forEach(image => {
            image.adjustments = { ...adjustments };
        });
        
        updateImageGrid();
        saveState();
        showToast('已应用到全部图片', 'success');
    });
    
    // 滤镜按钮
    DOM.filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            DOM.filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            AppState.currentFilter = btn.dataset.filter;
            updateSelectedAdjustments('filter', btn.dataset.filter);
            updateThumbnailsForSelected();
            saveState();
        });
    });
    
    // 重命名
    DOM.baseName.addEventListener('input', updateRenamePreview);
    DOM.startNumber.addEventListener('input', updateRenamePreview);
    DOM.numberDigits.addEventListener('change', updateRenamePreview);
    DOM.applyRenameBtn.addEventListener('click', applyRename);
    
    // 导出设置
    DOM.outputSize.addEventListener('change', () => {
        DOM.customSizeGroup.style.display = 
            DOM.outputSize.value === 'custom' ? 'block' : 'none';
    });
    
    // 下载按钮
    DOM.downloadBtn.addEventListener('click', exportImages);
    
    // 全选/取消全选
    DOM.selectAllBtn.addEventListener('click', () => {
        AppState.images.forEach(img => AppState.selectedIds.add(img.id));
        updateImageGrid();
        updateControlsFromSelection();
    });
    
    DOM.deselectAllBtn.addEventListener('click', () => {
        AppState.selectedIds.clear();
        updateImageGrid();
        updateControlsFromSelection();
    });
    
    // 删除选中
    DOM.deleteSelectedBtn.addEventListener('click', deleteSelectedImages);
    
    // 撤销/重做
    DOM.undoBtn.addEventListener('click', undo);
    DOM.redoBtn.addEventListener('click', redo);
    
    // 键盘快捷键
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
            if (e.key === 'z') {
                e.preventDefault();
                undo();
            } else if (e.key === 'y') {
                e.preventDefault();
                redo();
            }
        }
    });
    
    // 重置
    DOM.resetAllBtn.addEventListener('click', resetAll);
    
    // 模态框关闭
    DOM.closeBtn.addEventListener('click', () => {
        DOM.previewModal.classList.remove('active');
    });
    
    DOM.previewModal.addEventListener('click', (e) => {
        if (e.target === DOM.previewModal) {
            DOM.previewModal.classList.remove('active');
        }
    });
    
    // 初始化历史记录
    saveState();
    updateUndoRedoButtons();
    
    console.log('批量图片修改工具已初始化');
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
