<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Menu',
        items: [
            { label: 'Home', icon: 'fa-solid fa-house fa-fw', to: '/' },
            { label: 'Search', icon: 'fa-solid fa-magnifying-glass fa-fw', to: '/search' },
            { label: 'CV', icon: 'fa-solid fa-user fa-fw', to: '/cv' },
            { label: 'Circle', icon: 'fa-solid fa-users fa-fw', to: '/circle' },
            { label: 'Release', icon: 'fa-solid fa-calendar-days fa-fw', to: '/release' },
            { label: 'Tag', icon: 'fa-solid fa-tag fa-fw', to: '/tag' }
        ]
    },
    {
        label: 'User',
        items: [
            {label: 'Logout', icon: 'fa-solid fa-right-from-bracket fa-fw', to: '/logout'}
        ]
    }
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
