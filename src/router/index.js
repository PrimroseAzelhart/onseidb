import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import search from '@/views/search.vue'
import cv from '@/views/cv.vue'
import circle from '@/views/circle.vue'
import release from '@/views/release.vue'
import tag from '@/views/tag.vue'
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
