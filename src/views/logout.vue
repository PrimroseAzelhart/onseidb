<script setup>
import router from '@/router';
import { ref, inject, onMounted } from 'vue';
import axios from 'axios';

onMounted(() => {
    $cookies.remove('token');
});

</script>
