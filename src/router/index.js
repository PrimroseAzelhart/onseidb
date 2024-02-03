import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const home = () => import('@/views/home.vue');
const search = () => import('@/views/search.vue');
const cv = () => import('@/views/cv.vue');
const circle = () => import('@/views/circle.vue');
const release = () => import('@/views/release.vue');
const genre = () => import('@/views/genre.vue');
const login = () => import('@/views/login.vue');
const library = () => import('@/views/library.vue');
const database = () => import('@/views/database.vue');

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
                path: '/genre',
                name: 'Genre',
                component: genre
            },
            {
                path: '/library',
                name: 'Library',
                component: library
            },
            {
                path: '/database',
                name: 'Database',
                component: database
            }
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
    mode: 'history',
    routes
});

router.beforeEach((to, from, next) => {
    const isLogin = $cookies.get('auth');
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
