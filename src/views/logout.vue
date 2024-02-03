<script setup>
import router from '@/router';
import { inject } from 'vue';
import axios from 'axios';

const $cookies = inject('$cookies');

axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded';
// auth = $cookies.get('auth');

$cookies.remove('auth');
router.push('/login');

</script>

<template></template>
