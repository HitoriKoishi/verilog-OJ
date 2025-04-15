<script setup>
import { ref, onMounted, provide } from 'vue';
const website = ref({ website_footer: '© 2025 在线判题系统' }); // 默认值，可根据需要更改
const version = ref('1.0.0'); // 默认版本号
</script>

<template>
  <div class="footer-bottom">
    <p class="copyright text-secondary">© {{ new Date().getFullYear() }} Verilog OJ. All rights reserved.</p>
  </div>
</template>

<style scoped>

.footer-bottom {
  padding-top: var(--spacing-lg);
  padding-bottom: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
  text-align: center;
}

.copyright {
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
    text-align: center;
  }

  .footer-nav {
    align-items: center;
  }
}
</style>