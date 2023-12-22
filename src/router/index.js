import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layout/AppLayout.vue';

const routes = [
    {
        path: '/',
        component: AppLayout,
        children: [
            {
                path: '/',
                name: 'Home',
                component: Home
            }
        ]
    },
    {
        path: '/about',
        name: 'About',
        component: About
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
