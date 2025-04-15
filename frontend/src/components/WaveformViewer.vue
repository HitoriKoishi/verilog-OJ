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
      signal: []
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
  padding: 20px;
  background: #ffffff;
  border-radius: 6px;
  min-height: 200px;
}

.no-waveform {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #f5f5f5;
  border-radius: 6px;
}

/* 暗色主题支持 */
@media (prefers-color-scheme: dark) {
  .waveform-container {
    background: #1a1a1a;
  }

  .no-waveform {
    background: #2d2d2d;
    color: #999;
  }

  :deep(.WaveDrom) {
    background: #1a1a1a;
  }

  :deep(.WaveDrom text) {
    fill: #d4d4d4;
  }

  :deep(.WaveDrom path) {
    stroke: #666;
  }
}
</style>