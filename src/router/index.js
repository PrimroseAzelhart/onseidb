import home from '@/views/home.vue';
import search from '@/views/search.vue';
import cv from '@/views/cv.vue';
import circle from '@/views/circle.vue';
import release from '@/views/release.vue';
import tag from '@/views/tag.vue';
import login from '@/views/login.vue';

import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const routes = [
    {
        path: '/',
        component: AppLayout,
        children: [
            {
                path: '/',
                name: 'home',
                component: home
            },
            {
                path: '/search',
                name: 'Search',
                component: search
            },
            {
                path: '/cv',
                name: 'CV',
                component: cv
            },
            {
                path: '/circle',
                name: 'Circle',
                component: circle
            },
            {
                path: '/release',
                name: 'Release',
                component: release
            },
            {
                path: '/tag',
                name: 'Tag',
                component: tag
            },
        ]
    },
    {
        path: '/login',
        name: 'Login',
        component: login
    },
    {
        path: '/logout',
        name: 'Logout',
        component: login
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/'
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const isLogin = $cookies.get('token');
    if (isLogin) {
        next();
    } else {
        if (to.path !== '/login') {
            next('/login');
        } else {
            next();
        }
    }
});

export default router;
