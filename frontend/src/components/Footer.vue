<script setup>
</script>

<template>
  <div class="footer-bottom">
    <p class="copyright text-secondary">© {{ new Date().getFullYear() }} Veri-OJ. All rights reserved.</p>
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
  font-size: 1.0em;
  color: var(--text-secondary);
  font-family: var(--font-family-mono);
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