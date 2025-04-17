<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: '确认'
  },
  message: {
    type: String,
    required: true
  },
  confirmText: {
    type: String,
    default: '确定'
  },
  cancelText: {
    type: String,
    default: '取消'
  }
});

const visible = ref(false);
const isLeaving = ref(false);

const emit = defineEmits(['confirm', 'cancel']);

onMounted(() => {
  visible.value = true;
});

const handleConfirm = () => {
  hideDialog(() => emit('confirm'));
};

const handleCancel = () => {
  hideDialog(() => emit('cancel'));
};

const hideDialog = (callback) => {
  isLeaving.value = true;
  setTimeout(() => {
    visible.value = false;
    callback?.();
  }, 300);
};
</script>

<template>
  <transition name="dialog-fade">
    <div v-if="visible" class="confirm-overlay">
      <div :class="['confirm-dialog', { 'is-leaving': isLeaving }]">
        <h3 class="confirm-title">{{ title }}</h3>
        <div class="confirm-content">{{ message }}</div>
        <div class="confirm-buttons">
          <button class="btn-cancel" @click="handleCancel">{{ cancelText }}</button>
          <button class="btn-confirm" @click="handleConfirm">{{ confirmText }}</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: var(--z-modal);
}

.confirm-dialog {
  background-color: var(--surface-color);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  min-width: 300px;
  max-width: 90%;
  box-shadow: var(--shadow-lg);
}

.confirm-title {
  margin: 0;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
  font-size: 1.2rem;
}

.confirm-content {
  margin-bottom: var(--spacing-lg);
  color: var(--text-secondary);
}

.confirm-buttons {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
}

.btn-cancel,
.btn-confirm {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-sm);
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all var(--transition-normal);
}

.btn-cancel {
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
}

.btn-confirm {
  background-color: var(--primary-color);
  color: white;
}

.btn-cancel:hover {
  background-color: var(--hover-color);
}

.btn-confirm:hover {
  background-color: color-mix(in srgb, var(--primary-color) 80%, black);
}

.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity var(--transition-normal);
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;
}

.confirm-dialog.is-leaving {
  animation: scale-out 0.3s ease-in-out;
}

@keyframes scale-out {
  from {
    transform: scale(1);
    opacity: 1;
  }
  to {
    transform: scale(0.9);
    opacity: 0;
  }
}
</style> 