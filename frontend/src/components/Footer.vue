
<script setup>
import { ref, onMounted, provide } from 'vue';
const website = ref({ website_footer: '© 2025 在线判题系统' }); // 默认值，可根据需要更改
const version = ref('1.0.0'); // 默认版本号
</script>

<template>
    <div>
      <div class="footer">
        <p v-html="website.website_footer"></p>
        <p>Powered by <a href="https://github.com/HitoriKoishi/verilog-OJ">OnlineJudge</a>
          <span v-if="version">&nbsp; Version: {{ version }}</span>
        </p>
      </div>
    </div>
</template>


<style scoped>
.footer {
  position: flex;
  bottom: 0;
  margin-top: auto;
  padding: 20px 0;
  text-align: center;
  font-size: 0.9em;
  color: #666;
  background: #fff;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  flex: 0;
  width: 100%;
}
</style>