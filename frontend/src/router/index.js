import { createRouter, createWebHistory } from 'vue-router';

import {
    Home,
    UserProfile
} from '../views';

import ProblemList from '../views/ProblemList.vue';
import ProblemSubmit from '../views/ProblemSubmit.vue';
import About from '../views/About.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/problem/all',
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
        path: '/user/profile',
        name: 'UserProfile',
        component: UserProfile,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/about',
        name: 'About',
        component: About
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
