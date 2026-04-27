# 技术架构文档

> 项目：东方购物大屏 On-Air 分钟利润看板
> 状态：已确认

---

## 一、技术栈

| 技术 | 用途 | 加载方式 |
|------|------|----------|
| HTML5 | 页面结构 | 内嵌 |
| CSS3 | 样式 | 内嵌 `<style>` 标签 |
| JavaScript (ES6+) | 业务逻辑 | 内嵌 `<script>` 标签 |
| SheetJS (xlsx) | 浏览器端 Excel 解析 | CDN |
| Chart.js | 图表渲染 | CDN |
| GSAP | 动画效果 | CDN |
| Lucide Icons | 图标库 | CDN |
| Google Fonts | 字体（Noto Sans SC, JetBrains Mono） | CDN |

---

## 二、项目结构

本项目为单个 HTML 文件，所有代码内嵌。文件结构如下：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>东方购物大屏 On-Air 分钟利润看板</title>

    <!-- Google Fonts -->
    <link href="..." rel="stylesheet">

    <!-- Lucide Icons -->
    <script src="..."></script>

    <!-- Chart.js -->
    <script src="..."></script>

    <!-- GSAP -->
    <script src="..."></script>

    <!-- SheetJS -->
    <script src="..."></script>

    <style>
        /* 全部 CSS 样式 */
    </style>
</head>
<body>
    <!-- 页面 HTML 结构 -->

    <script>
        /* 全部 JavaScript 逻辑 */
    </script>
</body>
</html>
```

---

## 三、数据结构

### 3.1 全局 State 对象

```javascript
const state = {
    // 原始数据（Excel 解析后、清洗前）
    rawCurrentData: [],    // 当期原始数据数组
    rawCompareData: [],    // 对比期原始数据数组

    // 清洗后数据
    cleanedCurrentData: [],  // 当期清洗后数据
    cleanedCompareData: [],  // 对比期清洗后数据

    // 筛选器状态
    filters: {
        channel: '全部',       // 频道：全部 / 11 / 12
        broadcastType: '全部', // 直录播：全部 / 直播 / 录播
        timePeriod: '全部',    // 时间段：全部 / 白天 / 晚间
        dayType: '全部',       // 分类：全部 / 工作日 / 周末
        category: '全部',      // 大分类：全部 / 具体品类名
    },

    // 动态品类列表（从数据中提取）
    categoryList: [],

    // 文件上传状态
    files: {
        current: null,   // 当期文件 File 对象
        compare: null,   // 对比期文件 File 对象
    },

    // Chart.js 实例引用
    chartInstance: null,
};
```

### 3.2 单条数据记录结构

Excel 解析后的每行数据映射为以下 JavaScript 对象：

```javascript
{
    playDate: Date,           // 播放日期（Date 对象）
    playHour: Number,         // 播放开始小时（0-23）
    playType: String,         // 播放类型（原始值，如"再播放"或其他）
    mdName: String,           // md名（品类名称）
    channel: Number,          // 频道（11 或 12）
    onAirProfit: Number,      // On-Air利润（数值）
    hopePlayMinutes: Number,  // 希望播放（分）（数值）

    // 清洗阶段新增的衍生字段
    dayType: String,          // 分类：'工作日' 或 '周末'
    broadcastType: String,    // 直录播：'直播' 或 '录播'
    timePeriod: String,       // 时间段：'白天' 或 '晚间'
    minuteProfit: Number,     // 分钟利润 = onAirProfit / hopePlayMinutes
}
```

### 3.3 Excel 列名映射

Excel 文件中的列名与代码字段的对应关系：

| Excel 列名 | 代码字段 | 类型 |
|-------------|----------|------|
| 播放日期 | playDate | Date |
| 播放开始小时 | playHour | Number |
| 播放类型 | playType | String |
| md名 | mdName | String |
| 频道 | channel | Number |
| On-Air利润 | onAirProfit | Number |
| 希望播放（分） | hopePlayMinutes | Number |

---

## 四、关键实现说明

### 4.1 Excel 文件解析

使用 SheetJS 在浏览器端解析 Excel 文件，无需后端。

```javascript
/**
 * 解析上传的 Excel 文件
 * @param {File} file - 用户上传的文件对象
 * @returns {Promise<Array>} - 解析后的数据数组
 */
function parseExcelFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = function(e) {
            try {
                const data = new Uint8Array(e.target.result);
                const workbook = XLSX.read(data, { type: 'array' });
                const firstSheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheetName];
                const jsonData = XLSX.utils.sheet_to_json(worksheet);

                // 映射列名到标准字段
                const mappedData = jsonData.map(row => ({
                    playDate: parseDate(row['播放日期']),
                    playHour: Number(row['播放开始小时']),
                    playType: String(row['播放类型'] || '').trim(),
                    mdName: String(row['md名'] || '').trim(),
                    channel: Number(row['频道']),
                    onAirProfit: Number(row['On-Air利润']) || 0,
                    hopePlayMinutes: Number(row['希望播放（分）']) || 0,
                }));

                resolve(mappedData);
            } catch (error) {
                reject(new Error('Excel 文件解析失败: ' + error.message));
            }
        };

        reader.onerror = function() {
            reject(new Error('文件读取失败'));
        };

        reader.readAsArrayBuffer(file);
    });
}

/**
 * 解析 Excel 日期（处理 Date 对象和 Excel 日期序列号）
 * @param {*} value - Excel 中的日期值
 * @returns {Date} - JavaScript Date 对象
 */
function parseDate(value) {
    if (value instanceof Date) {
        return value;
    }
    if (typeof value === 'number') {
        // Excel 日期序列号转 JS Date
        // Excel 日期起始点为 1900-01-01，序列号 1
        const epoch = new Date(1899, 11, 30); // 1899-12-30
        return new Date(epoch.getTime() + value * 86400000);
    }
    if (typeof value === 'string') {
        return new Date(value);
    }
    return new Date(NaN);
}
```

### 4.2 数据清洗规则

按顺序执行以下清洗步骤：

```javascript
/**
 * 数据清洗流水线
 * @param {Array} rawData - 原始数据数组
 * @returns {Array} - 清洗后的数据数组
 */
function cleanData(rawData) {
    let data = [...rawData];

    // 步骤1：剔除"播放开始小时"为 1、2、3、4 的数据
    data = data.filter(row => ![1, 2, 3, 4].includes(row.playHour));

    // 步骤2：剔除"md名"为特定品类的数据
    const excludedCategories = ['全装修工程', '寿险', '汽车整车', '房产'];
    data = data.filter(row => !excludedCategories.includes(row.mdName));

    // 步骤3：计算"分类"字段（工作日/周末）
    data = data.map(row => {
        const day = row.playDate.getDay(); // 0=周日, 6=周六
        row.dayType = (day === 0 || day === 6) ? '周末' : '工作日';
        return row;
    });

    // 步骤4：计算"直录播"字段
    data = data.map(row => {
        row.broadcastType = (row.playType === '再播放') ? '录播' : '直播';
        return row;
    });

    // 步骤5：计算"时间段"字段
    data = data.map(row => {
        if (row.playHour >= 8 && row.playHour <= 17) {
            row.timePeriod = '白天';
        } else if (row.playHour >= 18 && row.playHour <= 23) {
            row.timePeriod = '晚间';
        }
        // 注意：0点、5-7点的数据保留但不标记时间段（不会被"白天"或"晚间"筛选命中）
        return row;
    });

    // 步骤6：计算"分钟利润"字段
    data = data.map(row => {
        if (row.hopePlayMinutes > 0) {
            row.minuteProfit = row.onAirProfit / row.hopePlayMinutes;
        } else {
            row.minuteProfit = 0; // 或标记为无效
        }
        return row;
    });

    return data;
}
```

### 4.3 数据聚合算法

#### 整体分钟利润聚合（区域1，不受筛选影响）

```javascript
/**
 * 计算整体分钟利润（按频道分组）
 * @returns {Object} - { channels: [{name, current, compare, yoyChange}] }
 */
function calculateOverallMinuteProfit() {
    const channels = [
        { name: '11频道', key: 11 },
        { name: '12频道', key: 12 },
        { name: '全部', key: 'all' },
    ];

    return channels.map(ch => {
        let currentData, compareData;

        if (ch.key === 'all') {
            currentData = state.cleanedCurrentData;
            compareData = state.cleanedCompareData;
        } else {
            currentData = state.cleanedCurrentData.filter(r => r.channel === ch.key);
            compareData = state.cleanedCompareData.filter(r => r.channel === ch.key);
        }

        const currentProfit = currentData.reduce((sum, r) => sum + r.onAirProfit, 0);
        const currentMinutes = currentData.reduce((sum, r) => sum + r.hopePlayMinutes, 0);
        const compareProfit = compareData.reduce((sum, r) => sum + r.onAirProfit, 0);
        const compareMinutes = compareData.reduce((sum, r) => sum + r.hopePlayMinutes, 0);

        const currentMP = currentMinutes > 0 ? currentProfit / currentMinutes : 0;
        const compareMP = compareMinutes > 0 ? compareProfit / compareMinutes : 0;
        const yoyChange = compareMP > 0 ? ((currentMP - compareMP) / compareMP) * 100 : 0;

        return {
            name: ch.name,
            current: Math.round(currentMP * 100) / 100,
            compare: Math.round(compareMP * 100) / 100,
            yoyChange: Math.round(yoyChange * 100) / 100,
        };
    });
}
```

#### 品类分钟利润聚合（区域2，受筛选影响）

```javascript
/**
 * 根据筛选条件过滤数据
 * @param {Array} data - 清洗后的数据
 * @returns {Array} - 过滤后的数据
 */
function applyFilters(data) {
    const { channel, broadcastType, timePeriod, dayType, category } = state.filters;

    return data.filter(row => {
        // 频道筛选
        if (channel !== '全部') {
            if (row.channel !== Number(channel)) return false;
        }
        // 直录播筛选
        if (broadcastType !== '全部') {
            if (row.broadcastType !== broadcastType) return false;
        }
        // 时间段筛选
        if (timePeriod !== '全部') {
            if (row.timePeriod !== timePeriod) return false;
        }
        // 分类筛选
        if (dayType !== '全部') {
            if (row.dayType !== dayType) return false;
        }
        // 大分类筛选
        if (category !== '全部') {
            if (row.mdName !== category) return false;
        }
        return true;
    });
}

/**
 * 计算品类分钟利润（受筛选影响）
 * @returns {Array} - [{mdName, currentMP, compareMP, yoyChange}]
 */
function calculateCategoryMinuteProfit() {
    const filteredCurrent = applyFilters(state.cleanedCurrentData);
    const filteredCompare = applyFilters(state.cleanedCompareData);

    // 获取所有品类（当期+对比期合并去重）
    const allCategories = new Set([
        ...filteredCurrent.map(r => r.mdName),
        ...filteredCompare.map(r => r.mdName),
    ]);

    const result = [];

    allCategories.forEach(mdName => {
        const currentRows = filteredCurrent.filter(r => r.mdName === mdName);
        const compareRows = filteredCompare.filter(r => r.mdName === mdName);

        const currentProfit = currentRows.reduce((sum, r) => sum + r.onAirProfit, 0);
        const currentMinutes = currentRows.reduce((sum, r) => sum + r.hopePlayMinutes, 0);
        const compareProfit = compareRows.reduce((sum, r) => sum + r.onAirProfit, 0);
        const compareMinutes = compareRows.reduce((sum, r) => sum + r.hopePlayMinutes, 0);

        const currentMP = currentMinutes > 0 ? currentProfit / currentMinutes : 0;
        const compareMP = compareMinutes > 0 ? compareProfit / compareMinutes : 0;

        let yoyChange = null;
        if (compareMP > 0) {
            yoyChange = Math.round(((currentMP - compareMP) / compareMP) * 10000) / 100;
        }

        result.push({
            mdName,
            currentMP: Math.round(currentMP * 100) / 100,
            compareMP: Math.round(compareMP * 100) / 100,
            yoyChange,
        });
    });

    // 按当期分钟利润降序排列
    result.sort((a, b) => b.currentMP - a.currentMP);

    return result;
}

/**
 * 计算品类播出档数（受筛选影响，排序跟随区域2）
 * @param {Array} sortedCategories - 区域2排序后的品类列表
 * @returns {Array} - [{mdName, currentCount, compareCount, diff}]
 */
function calculateCategoryBroadcastCount(sortedCategories) {
    const filteredCurrent = applyFilters(state.cleanedCurrentData);
    const filteredCompare = applyFilters(state.cleanedCompareData);

    return sortedCategories.map(({ mdName }) => {
        const currentCount = filteredCurrent.filter(r => r.mdName === mdName).length;
        const compareCount = filteredCompare.filter(r => r.mdName === mdName).length;

        return {
            mdName,
            currentCount,
            compareCount,
            diff: currentCount - compareCount,
        };
    });
}
```

### 4.4 Chart.js 混合图表配置

```javascript
/**
 * 渲染整体分钟利润混合图表
 * @param {Array} data - calculateOverallMinuteProfit() 的返回值
 */
function renderOverallChart(data) {
    const ctx = document.getElementById('overallChart').getContext('2d');

    // 销毁已有实例
    if (state.chartInstance) {
        state.chartInstance.destroy();
    }

    state.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.name),
            datasets: [
                {
                    label: '当期分钟利润',
                    type: 'bar',
                    data: data.map(d => d.current),
                    backgroundColor: '#3B82F6',
                    borderRadius: 6,
                    barPercentage: 0.6,
                    categoryPercentage: 0.7,
                    order: 2,
                },
                {
                    label: '对比期分钟利润',
                    type: 'bar',
                    data: data.map(d => d.compare),
                    backgroundColor: '#D1D5DB',
                    borderRadius: 6,
                    barPercentage: 0.6,
                    categoryPercentage: 0.7,
                    order: 3,
                },
                {
                    label: '同比变化%',
                    type: 'line',
                    data: data.map(d => d.yoyChange),
                    borderColor: '#F59E0B',
                    backgroundColor: 'rgba(245, 158, 11, 0.1)',
                    borderWidth: 3,
                    pointRadius: 6,
                    pointBackgroundColor: '#F59E0B',
                    pointBorderColor: '#FFFFFF',
                    pointBorderWidth: 2,
                    tension: 0.3,
                    fill: false,
                    yAxisID: 'yoy',
                    order: 1,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 800,
                easing: 'easeOutQuart',
            },
            plugins: {
                legend: {
                    position: 'top',
                    align: 'end',
                    labels: {
                        usePointStyle: true,
                        pointStyle: 'rectRounded',
                        padding: 20,
                        font: { size: 13, family: 'Noto Sans SC' },
                    },
                },
                tooltip: {
                    backgroundColor: '#1F2937',
                    titleFont: { size: 14, family: 'Noto Sans SC' },
                    bodyFont: { size: 13, family: 'JetBrains Mono' },
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            if (context.dataset.yAxisID === 'yoy') {
                                return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + '%';
                            }
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + ' 元/分钟';
                        },
                    },
                },
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        font: { size: 14, family: 'Noto Sans SC', weight: '600' },
                        color: '#374151',
                    },
                },
                y: {
                    position: 'left',
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '分钟利润（元/分钟）',
                        font: { size: 12, family: 'Noto Sans SC' },
                        color: '#6B7280',
                    },
                    grid: {
                        color: '#F3F4F6',
                        drawBorder: false,
                    },
                    ticks: {
                        font: { size: 12, family: 'JetBrains Mono' },
                        color: '#6B7280',
                    },
                },
                yoy: {
                    position: 'right',
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: '同比变化（%）',
                        font: { size: 12, family: 'Noto Sans SC' },
                        color: '#6B7280',
                    },
                    grid: { display: false },
                    ticks: {
                        font: { size: 12, family: 'JetBrains Mono' },
                        color: '#6B7280',
                        callback: function(value) { return value + '%'; },
                    },
                },
            },
        },
    });
}
```

### 4.5 筛选联动机制

```javascript
/**
 * 筛选器变更处理函数
 * 当任意筛选器值变化时调用
 */
function onFilterChange() {
    // 重新计算品类分钟利润
    const categoryProfitData = calculateCategoryMinuteProfit();

    // 重新计算播出档数（排序跟随品类分钟利润）
    const broadcastCountData = calculateCategoryBroadcastCount(categoryProfitData);

    // 渲染表格
    renderCategoryTable(categoryProfitData);
    renderBroadcastTable(broadcastCountData);

    // GSAP 表格更新动画
    gsap.from('.data-table tbody tr', {
        opacity: 0,
        y: 10,
        stagger: 0.03,
        duration: 0.3,
        ease: 'power2.out',
    });
}

/**
 * 初始化筛选器事件监听
 */
function initFilters() {
    const filterIds = ['filter-channel', 'filter-broadcast', 'filter-time', 'filter-day', 'filter-category'];

    filterIds.forEach(id => {
        const element = document.getElementById(id);
        element.addEventListener('change', function() {
            // 更新 state
            switch (id) {
                case 'filter-channel':
                    state.filters.channel = this.value;
                    break;
                case 'filter-broadcast':
                    state.filters.broadcastType = this.value;
                    break;
                case 'filter-time':
                    state.filters.timePeriod = this.value;
                    break;
                case 'filter-day':
                    state.filters.dayType = this.value;
                    break;
                case 'filter-category':
                    state.filters.category = this.value;
                    break;
            }
            // 触发联动更新
            onFilterChange();
        });
    });
}

/**
 * 提取动态品类列表并填充"大分类"筛选器
 */
function populateCategoryFilter() {
    const allMdNames = new Set([
        ...state.cleanedCurrentData.map(r => r.mdName),
        ...state.cleanedCompareData.map(r => r.mdName),
    ]);

    state.categoryList = Array.from(allMdNames).sort();

    const select = document.getElementById('filter-category');
    // 保留第一个"全部"选项，清除其余
    select.innerHTML = '<option value="全部">全部</option>';

    state.categoryList.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        select.appendChild(option);
    });
}
```

### 4.6 动画与交互

```javascript
/**
 * 页面入场动画
 */
function playEntranceAnimation() {
    const tl = gsap.timeline();

    tl.from('.chart-card', {
        opacity: 0,
        y: 30,
        duration: 0.6,
        ease: 'power3.out',
    })
    .from('.table-card', {
        opacity: 0,
        y: 30,
        duration: 0.6,
        stagger: 0.15,
        ease: 'power3.out',
    }, '-=0.3');
}

/**
 * 文件上传区域拖拽交互
 */
function initDragAndDrop() {
    const uploadAreas = document.querySelectorAll('.upload-area');

    uploadAreas.forEach(area => {
        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });

        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
        });

        area.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            const file = e.dataTransfer.files[0];
            handleFileUpload(this, file);
        });
    });
}

/**
 * Toast 提示
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    gsap.fromTo(toast,
        { opacity: 0, y: -20 },
        { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }
    );

    setTimeout(() => {
        gsap.to(toast, {
            opacity: 0,
            y: -20,
            duration: 0.3,
            ease: 'power2.in',
            onComplete: () => toast.remove(),
        });
    }, 3000);
}
```

---

## 五、CDN 依赖清单

| 库名 | 版本 | CDN 链接 | 用途 |
|------|------|----------|------|
| SheetJS (xlsx) | 0.18.5 | `https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js` | Excel 文件解析 |
| Chart.js | 4.4.1 | `https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js` | 图表渲染 |
| GSAP | 3.12.4 | `https://cdn.jsdelivr.net/npm/gsap@3.12.4/dist/gsap.min.js` | 动画效果 |
| Lucide Icons | 0.309.0 | `https://unpkg.com/lucide@0.309.0/dist/umd/lucide.min.js` | 图标 |
| Google Fonts - Noto Sans SC | - | `https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&display=swap` | 中文字体 |
| Google Fonts - JetBrains Mono | - | `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap` | 数字等宽字体 |

### HTML `<head>` 中的引用示例

```html
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;600;700&display=swap" rel="stylesheet">

<!-- Lucide Icons -->
<script src="https://unpkg.com/lucide@0.309.0/dist/umd/lucide.min.js"></script>

<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<!-- GSAP -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.4/dist/gsap.min.js"></script>

<!-- SheetJS -->
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
```

---

## 六、开发注意事项

### 6.1 数据处理

1. **Excel 日期解析：** Excel 中的日期可能以 Date 对象、数字序列号或字符串形式存在，`parseDate()` 函数需兼容所有格式
2. **除零保护：** 计算"分钟利润"时必须检查 `hopePlayMinutes > 0`，避免除以零
3. **同比变化分母保护：** 当对比期分钟利润为 0 时，同比变化应显示为 "--" 而非 Infinity 或 NaN
4. **数值精度：** 所有金额计算结果保留 2 位小数，使用 `Math.round(value * 100) / 100` 而非 `toFixed()` 避免浮点精度问题
5. **数据不可变性：** 清洗函数应返回新数组，不修改原始数据，以便筛选器重置时可以重新计算

### 6.2 性能优化

1. **Chart.js 实例管理：** 每次更新图表前必须先销毁旧实例（`chart.destroy()`），避免内存泄漏
2. **大数据量处理：** 如果数据量超过 10000 行，考虑使用 Web Worker 进行数据清洗，避免阻塞 UI 线程
3. **DOM 操作：** 表格渲染使用 DocumentFragment 批量插入 DOM，避免多次重排
4. **事件委托：** 筛选器事件使用事件委托模式，减少事件监听器数量

### 6.3 样式注意事项

1. **CSS 变量：** 使用 CSS 自定义属性（变量）统一管理颜色、间距、圆角等设计 token
2. **滚动条样式：** 表格容器使用自定义滚动条样式（`::-webkit-scrollbar`）
3. **数字对齐：** 表格中的数值列使用 `font-variant-numeric: tabular-nums` 确保等宽数字对齐
4. **打印适配：** 虽然本版本不包含打印功能，但应确保 `@media print` 下表格可正常显示

### 6.4 兼容性

1. **浏览器兼容：** 目标浏览器为 Chrome 90+、Edge 90+、Firefox 88+、Safari 14+
2. **ES6+ 语法：** 使用 `const/let`、箭头函数、模板字符串、解构赋值、`Set`、`Array.from()` 等现代语法
3. **不使用 TypeScript：** 本项目为纯 JavaScript，无需编译步骤
4. **CDN 可用性：** 所有 CDN 链接使用 jsdelivr 和 unpkg，确保国内可访问；如需离线使用，可将库文件下载到本地

### 6.5 错误处理

1. **文件格式校验：** 上传文件时检查扩展名是否为 `.xlsx` 或 `.xls`
2. **必要列校验：** 解析 Excel 后检查是否包含所有必要列，缺失时显示具体缺失的列名
3. **空文件处理：** 如果 Excel 文件为空或只有表头，显示友好提示
4. **异常捕获：** 所有异步操作（文件读取、数据解析）使用 try-catch 包裹，错误通过 Toast 提示用户
