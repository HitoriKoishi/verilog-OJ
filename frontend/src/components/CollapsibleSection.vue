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
  <div class="section" :class="[`status-${status}`]">
    <div class="section-header" @click="toggleExpand">
      <h2 class="text-primary">{{ title }}</h2>
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
  margin-bottom: var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  background-color: var(--background-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
}

/* 默认状态 */
.section.status-default {
  border-color: var(--border-color);
}

/* 成功状态 */
.section.status-success {
  animation: borderPulseSuccess 2s cubic-bezier(0.4, 0, 0.2, 1);
  border-color: var(--success-color);
  box-shadow: var(--success-color) 0px 0px 3px;
}

/* 失败状态 */
.section.status-error {
  animation: borderPulseError 2s cubic-bezier(0.4, 0, 0.2, 1);
  border-color: var(--error-color);
  box-shadow: var(--error-color) 0px 0px 3px;
}

/* 信息状态 */
.section.status-info {
  animation: borderPulseInfo 2s cubic-bezier(0.4, 0, 0.2, 1);
  border-color: var(--info-color);
  box-shadow: var(--info-color) 0px 0px 3px;
}

@keyframes borderPulseSuccess {
  0% {    border-color: var(--border-color);   box-shadow: 0px 0px 0px transparent;}
  50% {  border-color: var(--success-color);  box-shadow: var(--success-color) 0px 0px 5px;}
  100% {  border-color: var(--success-color);  box-shadow: var(--success-color) 0px 0px 3px;}
}

@keyframes borderPulseError {
  0% {    border-color: var(--border-color); box-shadow: 0px 0px 0px transparent;}
  50% {  border-color: var(--error-color);  box-shadow: var(--error-color) 0px 0px 5px;}
  100% {  border-color: var(--error-color);  box-shadow: var(--error-color) 0px 0px 3px;}
}

@keyframes borderPulseInfo {
  0% {    border-color: var(--border-color); box-shadow: 0px 0px 0px transparent;}
  50% {  border-color: var(--info-color); box-shadow: var(--info-color) 0px 0px 5px;}
  100% {  border-color: var(--info-color); box-shadow: var(--info-color) 0px 0px 3px;}
}


.section-header {
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--background-color);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  user-select: none;
  border-bottom: 1px solid var(--border-color);
  transition: all var(--transition-normal);
}

.section-header:hover {
  background-color: var(--surface-color);
}

.section-header h2 {
  margin: 0;
  font-size: 1.1em;
  font-weight: 500;
  transition: color var(--transition-normal);
}

.expand-icon {
  font-size: 16px;
  color: var(--text-secondary);
  transition: all var(--transition-normal);
}

.expand-icon.is-expanded {
  transform: rotate(90deg);
}

.section-content {
  overflow: hidden;
  transition: all var(--transition-normal);
  background-color: transparent;
}

.section-inner {
  padding: var(--spacing-md);
}

@media (max-width: 900px) {
  .section-inner {
    padding: var(--spacing-sm);
  }
}

.content-wrapper {
  overflow: visible; /* 允许内容溢出 */
}

.card-body {
  overflow: visible; /* 允许内容溢出 */
}
</style>