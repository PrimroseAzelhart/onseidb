<script setup>
import router from '@/router'
import { ref, inject } from 'vue';

const message = ref([]);
const auth = ref('');
const password = ref('');
const checked = ref(false);
const $cookies = inject('$cookies');

const addMessage = (type) => {
    if (type === 'error') {
        message.value = [{ severity: 'error', content: 'Authorization failed'}];
    }
};

const onLoginButtonClick = () => {
    if (auth.value === 'admin' && password.value === 'admin') {
        $cookies.set('token', 'logedin');
        router.push('/');
    } else {
        addMessage('error');
    }
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

                    <div class="flex align-items-center justify-content-between mb-5 gap-5">
                        <div class="flex align-items-center">
                            <Checkbox v-model="checked" inputId="rememberme" binary class="mr-2"></Checkbox>
                            <label for="rememberme">Remember me</label>
                        </div>
                        <!-- <a class="font-medium no-underline ml-2 text-right cursor-pointer" style="color: var(--primary-color)">Forgot password?</a> -->
                    </div>

                    <Button label="Sign In" class="w-full p-3 text-xl" @click="onLoginButtonClick()"></Button>
                    <transition-group name="p-message" tag="div">
                        <Message v-for="msg of message" :severity="msg.severity" :key="msg.content" :closable="false">{{ msg.content }}</Message>
                    </transition-group>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}
</style>
