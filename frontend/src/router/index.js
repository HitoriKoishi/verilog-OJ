import { createRouter, createWebHistory } from 'vue-router';

import {
    Home,
    UserProfile
} from '../views';

import ProblemList from '../views/ProblemList.vue';
import ProblemSubmit from '../views/ProblemSubmit.vue';
import About from '../views/About.vue';
import AdminPanel from '../views/AdminPanel.vue';

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
    },
    {
        path: '/admin',
        name: 'AdminPanel',
        component: AdminPanel,
        meta: { requiresAdmin: true }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const isLoggedIn = localStorage.getItem('user') !== null;
    const user = isLoggedIn ? JSON.parse(localStorage.getItem('user')) : null;
    const isAdmin = user?.is_admin;

    if (to.meta.requiresAdmin && !isAdmin) {
        next('/');
    } else {
        next();
    }
});

export default router;
