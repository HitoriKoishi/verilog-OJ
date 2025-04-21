<template>
  <div class="learning-path container">
    <h1 class="title">学习路径</h1>
    <div class="card-group">
      <div
        v-for="path in paths"
        :key="path.id"
        class="card card-hover card-interactive"
        @click="togglePath(path.id)"
      >
        <div class="card-header">
          <h2 class="card-title">{{ path.name }}</h2>
        </div>
        <div class="card-body">
          <p class="card-subtitle">{{ path.description }}</p>
          <div v-if="expanded === path.id" class="path-graph">
            <div class="chain">
              <template v-for="(prob, idx) in chain">
                <div
                  class="node"
                  @mouseover="showInfo(prob, $event)"
                  @mouseleave="hideInfo"
                  @click.stop="goToProblem(prob.id)"
                >
                  {{ prob.id }}
                </div>
                <span
                  v-if="idx < chain.length - 1"
                  class="arrow"
                >→</span>
              </template>
            </div>
            <div
              v-if="tooltip.visible"
              :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px' }"
              class="tooltip"
            >
              <strong>{{ tooltip.data.title }}</strong><br />
              难度：{{ tooltip.data.difficulty }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { learningPathApi } from '../api';
import { useRouter } from 'vue-router';

const paths = ref([]);
const expanded = ref(null);
const chain = ref([]);
const tooltip = ref({ visible: false, x: 0, y: 0, data: {} });
const router = useRouter();

const fetchPaths = async () => {
  const res = await learningPathApi.getPaths();
  paths.value = res.data;
};

const togglePath = async (id) => {
  if (expanded.value === id) {
    expanded.value = null;
    chain.value = [];
  } else {
    expanded.value = id;
    const res = await learningPathApi.getPathChain(id);
    chain.value = res.data.problems_chain;
  }
};

const showInfo = (prob, e) => {
  tooltip.value.visible = true;
  tooltip.value.data = prob;
  // 放置在节点右上方
  const rect = e.target.getBoundingClientRect();
  tooltip.value.x = rect.right + window.scrollX + 10;
  tooltip.value.y = rect.top + window.scrollY;
};

const hideInfo = () => {
  tooltip.value.visible = false;
};

const goToProblem = (id) => {
  router.push(`/problem/${id}`);
};

onMounted(() => {
  fetchPaths();
});
</script>

<style scoped>
.learning-path {
  padding: var(--spacing-lg);
}
.title {
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
}
.chain {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
}
.node {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  font-weight: bold;
  transition: transform var(--transition-fast);
}
.node:hover {
  transform: scale(1.1);
}
.arrow {
  font-size: 1.5rem;
  color: var(--text-secondary);
}
.tooltip {
  position: absolute;
  background: var(--surface-color);
  border: 1px solid var(--border-color);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  z-index: 100;
}
</style> 