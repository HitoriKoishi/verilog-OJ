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
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: 4px;
  color: white;
  font-size: 14px;
  z-index: 9999;
  cursor: pointer;
  box-shadow: 0 3px 6px rgba(0,0,0,0.2);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.message-alert.success {
  background-color: #1eac2a;
}

.message-alert.error {
  background-color: #d84130;
}

.message-alert.warning {
  background-color: #ffea61;
}

.message-alert.info {
  background-color: #70b0ff;
}

.message-fade-enter-active,
.message-fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
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
</style>