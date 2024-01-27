<script setup>

  import { inject } from 'vue';
  import { useLayout } from '@/layout/composables/layout'

  // const { changeTheme } = useLayout();

  const $cookies = inject('$cookies');
  $cookies.config('30d');

  // var themeSetting = $cookies.get('onseidb_theme');
  if (!$cookies.get('onseidb_theme')) {
    $cookies.set('onseidb_theme', { theme:'aura', color:'blue', dark:false});
  } else {
    // changeTheme(themeSetting.theme, themeSetting.color, themeSetting.dark);
  }

</script>

<template>
  <router-view></router-view>
</template>

<style scoped>

</style>
