<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  isExpanded: {
    type: Boolean,
    default: false
  },
  status: {
    type: String,
    default: 'default',  // 可选值: 'default', 'success', 'error'
  },
  isDarkMode: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:isExpanded']);

const toggleExpand = () => {
  emit('update:isExpanded', !props.isExpanded);
};

// 动画处理函数
const enter = (element) => {
  const height = element.scrollHeight;
  element.style.height = '0px';
  // 触发重绘
  element.offsetHeight;
  element.style.height = height + 'px';
};

const afterEnter = (element) => {
  element.style.height = 'auto';
};

const leave = (element) => {
  const height = element.scrollHeight;
  element.style.height = height + 'px';
  // 触发重绘
  element.offsetHeight;
  element.style.height = '0px';
};
</script>

<template>
  <div class="section" :class="[`status-${status}`, { 'dark-theme': isDarkMode }]">
    <div class="section-header" @click="toggleExpand">
      <h2>{{ title }}</h2>
      <span class="expand-icon" :class="{ 'is-expanded': isExpanded }">▶</span>
    </div>
    <transition 
      name="collapse"
      @enter="enter"
      @after-enter="afterEnter"
      @leave="leave"
    >
      <div v-show="isExpanded" class="section-content">
        <div class="section-inner">
          <slot></slot>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.section {
  margin-bottom: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: border-color 0.6s ease;
}

/* 默认状态 */
.section.status-default {
  border-color: #e0e0e0;
}

/* 成功状态 */
.section.status-success {
  border-color: #74e678;
  box-shadow: #4caf50 0 0 3px;
  animation: borderPulseSuccess 2s ease-out;
}

/* 失败状态 */
.section.status-error {
  border-color: #fd695e;
  box-shadow: #f44336 0 0 3px;
  animation: borderPulseError 2s ease-out;
}

@keyframes borderPulseSuccess {
  0% { border-color: #e0e0e0; }
  50% { border-color: #4caf50; }
  100% { border-color: #4caf50; }
}

@keyframes borderPulseError {
  0% { border-color: #e0e0e0; }
  50% { border-color: #f44336; }
  100% { border-color: #f44336; }
}

.section-header {
  padding: 12px 20px;
  background-color: #ffffff;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  user-select: none;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s ease;
}

.section-header:hover {
  background-color: #fafafa;
}

.section-header h2 {
  margin: 0;
  font-size: 1.1em;
  color: #333;
}

.expand-icon {
  font-size: 16px;
  color: #888;
  transition: transform 0.3s ease;
}

.expand-icon.is-expanded {
  transform: rotate(90deg);
}

.section-content {
  overflow: hidden;
  transition: height 0.3s ease-in-out;
  background-color: transparent;
}

.section-inner {
  padding: 20px;
}

/* 暗色主题样式 */
.dark-theme {
  border-color: #2d2d2d;
  background-color: #1a1a1a;
}

.dark-theme.status-default {
  border-color: #2d2d2d;
}

.dark-theme.status-success {
  border-color: #43a047;
}

.dark-theme.status-error {
  border-color: #e53935;
}

.dark-theme .section-header {
  background-color: #1a1a1a;
  border-bottom-color: #2d2d2d;
}

.dark-theme .section-header:hover {
  background-color: #242424;
}

.dark-theme .section-header h2 {
  color: #e0e0e0;
}

.dark-theme .expand-icon {
  color: #666;
}

@media (max-width: 900px) {
  .section-inner {
    padding: 15px;
  }
}
</style>