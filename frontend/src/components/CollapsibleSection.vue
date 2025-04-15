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
  transition: border-color var(--transition-normal);
}

/* 默认状态 */
.section.status-default {
  border-color: var(--border-color);
}

/* 成功状态 */
.section.status-success {
  border-color: var(--success-color);
  animation: borderPulseSuccess 2s ease-out;
}

/* 失败状态 */
.section.status-error {
  border-color: var(--error-color);
  animation: borderPulseError 2s ease-out;
}

@keyframes borderPulseSuccess {
  0% { border-color: var(--border-color); }
  50% { border-color: var(--success-color); }
  100% { border-color: var(--success-color); }
}

@keyframes borderPulseError {
  0% { border-color: var(--border-color); }
  50% { border-color: var(--error-color); }
  100% { border-color: var(--error-color); }
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
  transition: background-color var(--transition-fast);
}

.section-header:hover {
  background-color: var(--surface-color);
}

.section-header h2 {
  margin: 0;
  font-size: 1.1em;
  font-weight: 500;
}

.expand-icon {
  font-size: 16px;
  color: var(--text-secondary);
  transition: transform var(--transition-normal);
}

.expand-icon.is-expanded {
  transform: rotate(90deg);
}

.section-content {
  overflow: hidden;
  transition: height var(--transition-normal);
  background-color: transparent;
}

.section-inner {
  padding: var(--spacing-md);
}

/* 暗色主题支持 */
@media (prefers-color-scheme: dark) {
  .section {
    border-color: var(--border-color-dark);
    background-color: var(--background-color-dark);
  }

  .section.status-default {
    border-color: var(--border-color-dark);
  }
  
  .section.status-success {
    border-color: var(--success-color-dark);
  }
  
  .section.status-error {
    border-color: var(--error-color-dark);
  }

  @keyframes borderPulseSuccess {
    0% { border-color: var(--border-color-dark); }
    50% { border-color: var(--success-color-dark); }
    100% { border-color: var(--success-color-dark); }
  }

  @keyframes borderPulseError {
    0% { border-color: var(--border-color-dark); }
    50% { border-color: var(--error-color-dark); }
    100% { border-color: var(--error-color-dark); }
  }

  .section-header {
    background-color: var(--background-color-dark);
    border-bottom-color: var(--border-color-dark);
  }

  .section-header:hover {
    border-color: var(--border-color-dark);
    background-color: var(--surface-color-dark);
  }

  .section-header h2 {
    border-color: var(--border-color-dark);
    color: var(--text-primary-dark);
  }

  .expand-icon {
    color: var(--text-secondary-dark);
  }
}

@media (max-width: 900px) {
  .section-inner {
    padding: var(--spacing-sm);
  }
}
</style>