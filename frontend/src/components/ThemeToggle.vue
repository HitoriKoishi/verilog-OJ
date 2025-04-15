<template>
  <button class="theme-toggle" @click="toggleTheme" :title="isDarkMode ? '切换到浅色模式' : '切换到深色模式'">
    <svg v-if="isDarkMode" class="icon" viewBox="0 0 24 24">
      <path fill="currentColor" d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5s5-2.24 5-5s-2.24-5-5-5m0 2c1.66 0 3 1.34 3 3s-1.34 3-3 3s-3-1.34-3-3s1.34-3 3-3M2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1m20 0h-2c-.55 0-1-.45-1-1s.45-1 1-1h2c.55 0 1 .45 1 1s-.45 1-1 1M11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1m0 20v-2c0-.55.45-1 1-1s1 .45 1 1v2c0 .55-.45 1-1 1s-1-.45-1-1M5.99 4.58c-.39-.39-1.03-.39-1.41 0c-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58m12.37 12.37c-.39-.39-1.03-.39-1.41 0c-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0c.39-.39.39-1.03 0-1.41l-1.06-1.06m1.06-10.96l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06c.39-.39.39-1.03 0-1.41c-.39-.39-1.03-.39-1.41 0M7.05 18.36l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06c.39-.39.39-1.03 0-1.41s-1.03-.39-1.41 0z"/>
    </svg>
    <svg v-else class="icon" viewBox="0 0 24 24">
      <path fill="currentColor" d="M11.38 2.019a7.5 7.5 0 1 0 10.6 10.6C21.662 17.854 17.316 22 12.001 22C6.477 22 2 17.523 2 12c0-5.315 4.146-9.661 9.38-9.981z"/>
    </svg>
  </button>
</template>

<script setup>
import { inject } from 'vue';

const { isDarkMode, toggleTheme } = inject('theme');
</script>

<style scoped>
.theme-toggle {
  position: fixed;
  bottom: var(--spacing-lg);
  right: var(--spacing-lg);
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background-color: var(--background-color);
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-fast);
  z-index: var(--z-fixed);
  border: 1px solid var(--border-color);
}

.theme-toggle:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  background-color: var(--surface-color);
}

.theme-toggle:active {
  transform: translateY(0);
}

.icon {
  width: 24px;
  height: 24px;
  transition: transform var(--transition-fast);
}

.theme-toggle:hover .icon {
  transform: rotate(30deg);
}

@media (max-width: 768px) {
  .theme-toggle {
    bottom: var(--spacing-md);
    right: var(--spacing-md);
    width: 40px;
    height: 40px;
  }

  .icon {
    width: 20px;
    height: 20px;
  }
}

</style>