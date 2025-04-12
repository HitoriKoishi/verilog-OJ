import { createRouter, createWebHistory } from 'vue-router';

import {
    Home,
    UserProfile
} from '../views';

import ProblemList from '../views/ProblemList.vue';
import ProblemSubmit from '../views/ProblemSubmit.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/problems',
        name: 'ProblemList',
        component: ProblemList
    },
    {
        path: '/problem/:id',
        name: 'ProblemSubmit',
        component: ProblemSubmit,
        props: true
    },
    {
        path: '/profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: {
            requiresAuth: true // 标记该路由需要登录权限
        }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
