<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'info'  // 可选值: success, error, warning, info
  },
  message: {
    type: String,
    required: true
  },
  duration: {
    type: Number,
    default: 3000
  }
});

const visible = ref(false);
const isLeaving = ref(false);

const emit = defineEmits(['close']);

onMounted(() => {
  visible.value = true;
  if (props.duration > 0) {
    setTimeout(() => {
      hideMessage();
    }, props.duration);
  }
});

const hideMessage = () => {
  isLeaving.value = true;
  setTimeout(() => {
    visible.value = false;
    emit('close');
  }, 300);
};
</script>

<template>
  <transition name="message-fade">
    <div v-if="visible" 
         :class="['message-alert', type, { 'is-leaving': isLeaving }]"
         @click="hideMessage">
      <span class="message-content">{{ message }}</span>
    </div>
  </transition>
</template>

<style scoped>
.message-alert {
  position: fixed;
  left: 50%;
  transform: translateX(-50%);
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-sm);
  color: white;
  font-size: 0.875rem;
  z-index: var(--z-tooltip);
  cursor: pointer;
  box-shadow: var(--shadow-md);
  pointer-events: auto;
  transition: all var(--transition-normal);
}

.message-alert.success {
  background-color: var(--success-color);
}

.message-alert.error {
  background-color: var(--error-color);
}

.message-alert.warning {
  background-color: var(--warning-color);
}

.message-alert.info {
  background-color: var(--info-color);
}

.message-fade-enter-active,
.message-fade-leave-active {
  transition: 
    opacity var(--transition-normal),
    transform var(--transition-normal);
}

.message-fade-enter-from,
.message-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px);
}

.is-leaving {
  opacity: 0;
  transform: translate(-50%, -20px);
}

.message-content {
  display: inline-block;
  vertical-align: middle;
  line-height: 1.4;
}
</style>