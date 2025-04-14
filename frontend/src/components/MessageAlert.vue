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
  },
  onClose: {
    type: Function,
    default: () => {}
  }
})

const visible = ref(false)
const isLeaving = ref(false)

onMounted(() => {
  visible.value = true
  if (props.duration > 0) {
    setTimeout(() => {
      hideMessage()
    }, props.duration)
  }
})

const hideMessage = () => {
  isLeaving.value = true
  setTimeout(() => {
    visible.value = false
    props.onClose()
  }, 300)
}
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
  padding: 12px 24px;
  border-radius: 4px;
  color: white;
  font-size: 14px;
  z-index: 9999;
  cursor: pointer;
  box-shadow: 0 3px 6px rgba(0,0,0,0.2);
  /* 移除 transition，由 message-fade 类控制 */
  pointer-events: auto;
}

.message-alert.success {
  background-color: #1eac2a;
}

.message-alert.error {
  background-color: #d84130;
}

.message-alert.warning {
  background-color: #9e830b;
}

.message-alert.info {
  background-color: #70b0ff;
}

.message-fade-enter-active {
  transition: opacity 0.3s ease-out, transform 0.3s ease-out;
}

.message-fade-leave-active {
  transition: opacity 0.3s ease-in, transform 0.3s ease-in;
  pointer-events: none;
}

.message-fade-enter-from {
  opacity: 0;
  transform: translate(-50%, -20px);
}

.message-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px);
}
</style>