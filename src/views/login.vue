<script setup>
import router from '@/router';
import { ref, inject, onMounted } from 'vue';
import axios from 'axios';

import Password from 'primevue/password';

const message = ref([]);
const auth = ref('');
const password = ref('');
const loginLoading = ref(false);

const $cookies = inject('$cookies');

const msgText = {
    'failed': 'Authorization failed!',
    'empty': 'Username and password cannot be empty!',
    'error': 'Server has encountered internal error!',
    'success': 'Login successfully, redirecting to homepage...'
};

axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded';

onMounted(() => {
    $cookies.remove('token');
});

const addMessage = (type, level) => {
    message.value = [{ severity: level, content: msgText[type]}];
};

const onLoginButtonClick = () => {
    if (!auth.value || !password.value) {
        addMessage('empty', 'error');
        return;
    }
    message.value = [];
    loginLoading.value = true;
    axios.post('https://api.onsei.fans/login', {
        username: auth.value,
        password: password.value
    })
    .then(function (response) {
        const res = response.data;
        if (res.code !== 0) {
            addMessage('failed', 'error');
        } else {
            addMessage('success', 'success');
            $cookies.set('auth', {'user': res.user, 'token': res.token});
            setTimeout(() => {
                router.push('/');
            }, 1000);
        }
    })
    .catch(function (error) {
        addMessage('error', 'error')
    });
    loginLoading.value = false;
}

</script>

<template>
    <div class="surface-ground flex align-items-center justify-content-center min-h-screen min-w-screen overflow-hidden">
        <div class="flex flex-column align-items-center justify-content-center">
            <img :src="'onseidb-logo.svg'" alt="OnseiDB logo" class="mb-5 w-8rem flex-shrink-0" />
            <div class="w-full surface-card py-8 px-5 sm:px-8" style="border-radius: 53px">
                <div class="text-center mb-5">
                    <!-- <img src="/demo/images/login/avatar.png" alt="Image" height="50" class="mb-3" /> -->
                    <div class="text-900 text-3xl font-medium mb-3">Welcome to OnseiDB!</div>
                    <span class="text-600 font-medium">Sign in to continue</span>
                </div>

                <div>
                    <label for="auth" class="block text-900 text-xl font-medium mb-2">Email or username</label>
                    <InputText id="auth" type="text" class="w-full md:w-30rem mb-5" style="padding: 1rem" v-model="auth" />

                    <label for="password" class="block text-900 font-medium text-xl mb-2">Password</label>
                    <Password inputId="password" v-model="password" :toggleMask="true" class="w-full mb-3" inputClass="w-full" :inputStyle="{ padding: '1rem' }" :feedback="false"></Password>

                    <Button label="Sign In" class="w-full p-3 text-xl" @click="onLoginButtonClick()" :loading="loginLoading" />
                    <transition-group name="p-message" tag="div">
                        <Message v-for="msg of message" :severity="msg.severity" :key="msg.content" :closable="false">{{ msg.content }}</Message>
                    </transition-group>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped></style>
