<script setup>
import { ref, onMounted, watch } from 'vue';
import WaveDrom from 'wavedrom';
import * as vcdParser from 'vcd-parser';

const props = defineProps({
    vcdContent: {
        type: String,
        default: ''
    }
});

const waveformElement = ref(null);

// 将 VCD 内容转换为 WaveDrom JSON 格式
const convertVcdToWaveDrom = (vcdContent) => {
  try {
    const vcd = vcdParser.parse(vcdContent);
    const waves = {
      signal: [],
      config: {
        hscale: 2
      }
    };

        // 遍历 VCD 中的信号
        Object.keys(vcd.signals).forEach(signalName => {
            const signal = vcd.signals[signalName];
            const wave = {
                name: signalName,
                wave: '',
                data: []
            };

            // 转换信号变化为 WaveDrom 格式
            signal.changes.forEach((change, index) => {
                if (index === 0 || change.value !== signal.changes[index - 1].value) {
                    wave.wave += change.value === '1' ? 'h' : 'l';
                    wave.data.push(change.value);
                } else {
                    wave.wave += '.';
                }
            });

            waves.signal.push(wave);
        });

        return waves;
    } catch (err) {
        console.error('VCD 解析错误:', err);
        return null;
    }
};

// 渲染波形
const renderWaveform = () => {
    if (!props.vcdContent || !waveformElement.value) return;

    try {
        const waves = convertVcdToWaveDrom(props.vcdContent);
        if (waves) {
            WaveDrom.RenderWaveForm(waveformElement.value, waves, {
                skin: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'default'
            });
        }
    } catch (err) {
        console.error('波形渲染错误:', err);
    }
};

// 监听 VCD 内容变化
watch(() => props.vcdContent, (newVal) => {
    if (newVal) {
        renderWaveform();
    }
});

// 监听主题变化
const setupThemeListener = () => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', renderWaveform);
};

onMounted(() => {
    setupThemeListener();
    if (props.vcdContent) {
        renderWaveform();
    }
});
</script>

<template>
    <div class="waveform-viewer">
        <div v-if="vcdContent" ref="waveformElement" class="waveform-container"></div>
        <div v-else class="no-waveform">
            暂无波形数据
        </div>
    </div>
</template>

<style scoped>
.waveform-viewer {
    width: 100%;
    overflow: auto;
}

.waveform-container {
  padding: var(--spacing-lg);
  background-color: var(--background-color);
  min-height: 200px;
}

.no-waveform {
  text-align: center;
  padding: var(--spacing-xl);
  background-color: var(--surface-color);
}

/* 波形样式定制 */
:deep(.WaveDrom) {
  background-color: var(--background-color);
}

:deep(.WaveDrom text) {
  fill: var(--text-primary);
  font-family: var(--font-family-code);
}

:deep(.WaveDrom path) {
  stroke: var(--text-secondary);
}

:deep(.WaveDrom .h1) {
  fill: var(--success-color);
}

:deep(.WaveDrom .h0) {
  fill: var(--error-color);
}

:deep(.WaveDrom .grid) {
  stroke: var(--border-color);
  stroke-width: 0.5;
}

:deep(.WaveDrom .time) {
  fill: var(--text-secondary);
  font-size: 12px;
}

:deep(.WaveDrom .signal) {
  fill: var(--text-primary);
  font-size: 14px;
}

/* 支持滚动 */
:deep(.WaveDrom svg) {
  max-width: none;
  overflow-x: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .waveform-container {
    padding: var(--spacing-md);
  }
  
  :deep(.WaveDrom text) {
    font-size: 12px;
  }
}
</style>