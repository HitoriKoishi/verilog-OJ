<script setup>
import { ref, onMounted, watch } from 'vue';
import * as vcdParser from 'vcd-parser';
import message from '../utils/message';

const props = defineProps({
    vcdContent: {
        type: String,
        default: ''
    }
});

const waveformElement = ref(null);
// 在组件中增加 WaveDrom 加载状态跟踪
const isWaveDromReady = ref(false);

// 独立初始化 WaveDrom 加载检查
const initWaveDrom = () => {
  if (typeof WaveDrom !== 'undefined') {
    isWaveDromReady.value = true;
    return;
  }
  setTimeout(initWaveDrom, 100); // 持续检查直到加载完成
};

// 波形字符转换（根据信号位宽决定显示方式）
const convertToWaveChar = (value, isMultiBit) => {
    // 多维信号始终标记为数据段
    if (isMultiBit) return '='; 
    // 单维信号处理逻辑
    if (value === '1') return '1';
    if (value === '0') return '0';
    return value[0] || 'x'; // 取第一个字符处理x/z
};

// 工具函数：二进制转无符号十进制（处理x/z）
const binToUnsignedDec = (binStr) => {
    if (binStr.includes('x')) return 'x';
    if (binStr.includes('z')) return 'z';
    return binStr ? (parseInt(binStr, 2) >>> 0).toString() : 'x';
};

// 将 VCD 内容转换为 WaveDrom JSON 格式
// 将 VCD 内容转换为 WaveDrom JSON 格式
const convertVcdToWaveDrom = async (vcdContent) => {
    if (!vcdContent) return null;
    
    try {
        const dumpoffIndex = vcdContent.indexOf('$dumpoff');
        if (dumpoffIndex !== -1) {
            vcdContent = vcdContent.substring(0, dumpoffIndex);
        }
        console.log('VCD 内容:', vcdContent);
        const vcd = await vcdParser.parse(vcdContent, { compress: true });
        console.log('解析后的 VCD 数据:', vcd);
        if (!vcd.signal?.length) {
            throw new Error('无效的 VCD 数据格式');
        }
        console.log('解析后的 VCD 数据:', vcd);
        // 计算整个波形的时间总长度
        let maxTime = 0;
        vcd.signal.forEach(signal => {
            if (signal.wave) {
                signal.wave.forEach(([timeStr]) => {
                    const time = parseInt(timeStr);
                    if (time > maxTime) maxTime = time;
                });
            }
        });
        console.log('最大时间:', maxTime);
        const signals = vcd.signal.map(signal => {
        if (!signal?.signalName || !signal?.wave) return null;
        // 关键修改点：通过位宽判断信号维度
        const isMultiBit = signal.size > 1; // 假设 vcd-parser 提供 size 属性
        const wave = { name: signal.signalName, wave: '', data: [] };
        let lastTime = -1;
        let maxSignalTime = 0;
        console.log('信号名称:', signal.signalName, '波形数据:', signal.wave);
        signal.wave.forEach(([time, value]) => {
            const timeNum = parseInt(time);
            maxSignalTime = Math.max(maxSignalTime, timeNum);
            // 时间间隔处理
            if (lastTime !== -1) {
                const timeDiff = Math.ceil((timeNum - lastTime) / 5000);
                wave.wave += '.'.repeat(Math.max(0, timeDiff - 1)); // 防止负数
            }
            // 波形字符处理
            console.log('当前时间:', timeNum, '信号值:', value);
            const waveChar = convertToWaveChar(value, isMultiBit);
            console.log('波形字符:', waveChar);
            wave.wave += waveChar;
            // 多维信号值转换
            if (isMultiBit) {
                console.log('多维信号值转换:', value);
                wave.data.push(binToUnsignedDec(value));
                console.log('转换后的值:', wave.data);
            }
            lastTime = timeNum;
        });
        // 关键修复：强制填充到全局最大时间
        if (lastTime < maxTime) {
            const timeDiff = Math.ceil((maxTime - lastTime) / 5000); // 使用全局 maxTime
            wave.wave += '.'.repeat(timeDiff);
        }
        return wave;
        }).filter(Boolean);
        return {
            signal: signals,
            config: { 
                hscale: 1,
                displayWidth: '100%'
            }
        };
    } catch (err) {
        console.error('VCD 解析错误:', err);
        message.error('VCD 解析错误: ' + (err.message || '未知错误'));
        return null;
    }
};

// 修改渲染函数
const renderWaveform = async () => {
  if (!props.vcdContent) return;
  
  try {
    // 等待 WaveDrom 和 DOM 元素就绪
    if (typeof WaveDrom === 'undefined' || !waveformElement.value) {
      setTimeout(renderWaveform, 100); // 延迟重试
      return;
    }

    // 清空前再次确认元素存在
    if (waveformElement.value) {
      waveformElement.value.innerHTML = '';
    }
    
    // 转换数据
    const waveData = await convertVcdToWaveDrom(props.vcdContent);
    if (!waveData) return;

    // 创建并插入渲染元素
    const waveScript = document.createElement('script');
    waveScript.type = 'WaveDrom';
    waveScript.text = JSON.stringify(waveData);
    waveformElement.value.appendChild(waveScript);
    
    // 强制渲染
    WaveDrom.ProcessAll();
  } catch (err) {
    console.error('渲染失败:', err);
  }
};

// 使用 nextTick 确保 DOM 更新
import { nextTick } from 'vue';

watch(() => props.vcdContent, async (newVal) => {
  if (newVal) {
    await nextTick(); // 等待 DOM 更新
    renderWaveform();
  }
});

// 在组件挂载时启动初始化
onMounted(() => {
  initWaveDrom();
  if (props.vcdContent) renderWaveform();
});
</script>

<template>
    <div class="waveform-viewer">
        <div v-if="vcdContent" ref="waveformElement" class="waveform-container"></div>
        <p v-else class="no-waveform text-secondary">暂无波形数据</p>
    </div>
</template>

<style>
.waveform-viewer {
    width: 100%;
    max-width: 100%;
    overflow: auto;
    padding-bottom: var(--spacing-md);
    background: var(--background-color);
}

.waveform-container {
    padding: var(--spacing-lg);
    min-height: 200px;
    width: max-content;
    min-width: 100%;
}

/* 波形图样式 */
.WaveDrom {
    min-width: max-content;
    display: block;
    background: var(--background-color);
}

.WaveDrom svg {
    max-width: none;
    min-width: max-content;
    display: block;
}

.no-waveform {
    text-align: center;
    padding: var(--spacing-xl);
}

@media (max-width: 768px) {
    .waveform-container {
        padding: var(--spacing-md);
    }
}
</style>