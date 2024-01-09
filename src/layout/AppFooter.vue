<script setup>
import { useLayout } from '@/layout/composables/layout';
import { computed } from 'vue';

const { layoutConfig } = useLayout();

const logoUrl = computed(() => {
    return `layout/images/${layoutConfig.darkTheme.value ? 'logo-white' : 'logo-dark'}.svg`;
});
</script>

<template>
    <div class="layout-footer" style="user-select: none">
        <img :src="'onseidb-logo.svg'" alt="logo" height="20" class="mr-2" />
        by miku39 using primevue
    </div>
</template>

<style lang="scss" scoped>

</style>
