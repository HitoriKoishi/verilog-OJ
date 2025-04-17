import { ref } from 'vue';
import { problemApi } from '../api';

// 从localStorage加载保存的标签
const loadSavedTags = () => {
    try {
        const savedTags = localStorage.getItem('selectedTags');
        return savedTags ? JSON.parse(savedTags) : [];
    } catch (e) {
        console.error('加载保存的标签失败:', e);
        return [];
    }
};

// 创建响应式状态
const selectedTags = ref(loadSavedTags());
const currentProblemList = ref([]);
const allProblems = ref([]); // 存储所有题目

// 导出状态和方法
export const problemState = {
    selectedTags,
    currentProblemList,
    allProblems,
    
    // 初始化所有题目列表
    async initializeProblems() {
        try {
            const response = await problemApi.getProblems();
            allProblems.value = response.data;
            // 如果当前筛选列表为空，使用完整列表
            if (currentProblemList.value.length === 0) {
                currentProblemList.value = response.data;
            }
            return true;
        } catch (e) {
            console.error('初始化题目列表失败:', e);
            return false;
        }
    },
    
    // 设置选中的标签
    setSelectedTags(tags) {
        selectedTags.value = tags;
        // 保存到localStorage
        try {
            localStorage.setItem('selectedTags', JSON.stringify(tags));
        } catch (e) {
            console.error('保存标签失败:', e);
        }
    },
    
    // 设置当前问题列表
    setCurrentProblemList(problems) {
        currentProblemList.value = problems;
    },
    
    // 获取下一题的ID
    getNextProblemId(currentId) {
        // 优先使用当前筛选后的列表
        const list = currentProblemList.value.length > 0 ? 
                    currentProblemList.value : 
                    allProblems.value;
        
        if (!list.length) return null;
        
        const currentIndex = list.findIndex(p => p.id === currentId);
        if (currentIndex === -1 || currentIndex === list.length - 1) {
            return null;
        }
        
        return list[currentIndex + 1].id;
    },

    // 清除所有标签选择
    clearTags() {
        selectedTags.value = [];
        localStorage.removeItem('selectedTags');
        // 重置为完整题目列表
        currentProblemList.value = [...allProblems.value];
    }
}; 