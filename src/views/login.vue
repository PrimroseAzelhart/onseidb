<script setup>
import router from '@/router';
import { ref, inject, onMounted } from 'vue';
import { databaseService } from '@/service/api.js'

import Password from 'primevue/password';

const message = ref([]);
const auth = ref('');
const password = ref('');
const registerUser = ref('');
const registerPwd = ref('');
const code = ref('');
const loginLoading = ref(false);
const registerLoading = ref(false);
const loginShow = ref(true);
const registerShow = ref(false);

const $cookies = inject('$cookies');

const db = new databaseService();

const msgText = {
    'failed': 'Authorization failed!',
    'empty': 'Username and password cannot be empty!',
    'error': 'Server has encountered an internal error!',
    'success': 'Login successfully, redirecting to homepage...',
    'format_error': 'Invitation code format is invalid!',
    'invalid_code': 'The invitation code is invalid!',
    'user_exist': 'This username is already been used!',
    'register_success': 'Registration complete, back to login page to login!'
};

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
    db.login({
        username: auth.value,
        password: password.value
    })
    .then(function (response) {
        if (response.err_code !== 0) {
            addMessage('failed', 'error');
        } else {
            addMessage('success', 'success');
            $cookies.set('auth', {'user': response.user, 'token': response.token});
            setTimeout(() => {
                router.push('/');
            }, 1000);
        }
    })
    .catch(function (error) {
        addMessage('error', 'error');
    });
    loginLoading.value = false;
};

const onRegisterButtonClick = () => {
    if (!registerUser.value || !registerPwd.value) {
        addMessage('empty', 'error');
        return;
    }
    if (code.value.length != 32) {
        addMessage('format_error', 'error');
        return;
    }
    message.value = [];
    registerLoading.value = true;
    db.register({
        username: registerUser.value,
        password: registerPwd.value,
        invitation_code: code.value
    })
    .then(function (response) {
        if (response.err_code == 1) {
            addMessage('invalid_code', 'error');
        } else if (response.err_code == 2) {
            addMessage('user_exist', 'error');
        } else {
            addMessage('register_success', 'success');
        }
    })
    .catch(function (error) {
        addMessage('error', 'error');
    });
    registerLoading.value = false;
}

const toggleRegister = (show) => {
    message.value = [];
    if (show) {
        loginShow.value = false;
        setTimeout(() => {
            registerShow.value = true;
        }, 500);
    } else {
        registerShow.value = false;
        setTimeout(() => {
            loginShow.value = true;
        }, 500);
    }
};

</script>

<template>
    <div class="flex align-items-center justify-content-center">
        <Transition name="slide-left">
            <div class="card flex-column align-items-center justify-content-center" style="max-width: 30rem;" v-show="loginShow">
                <div class="w-full px-3 pt-4 pb-2">
                    <div class="text-center mb-5">
                        <div class="text-900 text-3xl font-medium mb-3">Welcome to OnseiDB!</div>
                        <span class="text-600 font-medium">Sign in to continue</span>
                    </div>

                    <div>
                        <label for="auth" class="text-900 text-xl font-medium mb-2">Username</label>
                        <InputText id="auth" type="text" class="w-full my-3" v-model="auth" />

                        <label for="password" class="text-900 font-medium text-xl mb-2">Password</label>
                        <Password inputId="password" v-model="password" :toggleMask="true" class="w-full my-3" inputClass="w-full" :feedback="false"></Password>

                        <Button label="Sign In" class="w-full p-3 text-xl" @click="onLoginButtonClick()" :loading="loginLoading" />
                        <div class="flex justify-content-between mt-3">
                            <Button label="Forget password" text />
                            <Button label="Register" text @click="toggleRegister(true)" />
                        </div>

                        <transition-group name="p-message" tag="div">
                            <Message v-for="msg of message" :severity="msg.severity" :key="msg.content" :closable="false">{{ msg.content }}</Message>
                        </transition-group>
                    </div>
                </div>
            </div>
        </Transition>

        <Transition name="slide-right">
            <div class="card flex-column align-items-center justify-content-center" style="max-width: 30rem;" v-show="registerShow">
                <div class="w-full px-3 pt-4 pb-2">
                    <div class="text-center mb-5 text-900 text-3xl font-medium">Register</div>

                    <label for="auth" class="text-900 text-xl font-medium mb-2">Username</label>
                    <InputText id="auth" type="text" class="w-full my-3" v-model="registerUser" />

                    <label for="password" class="text-900 font-medium text-xl mb-2">Password</label>
                    <Password inputId="password" v-model="registerPwd" :toggleMask="true" class="w-full my-3" inputClass="w-full" :feedback="false"></Password>

                    <label for="code" class="text-900 text-xl font-medium mb-2">Invitation code</label>
                    <InputText id="code" type="text" class="w-full my-3" v-model="code" />

                    <Button label="Register" class="w-full p-3 text-xl" @click="onRegisterButtonClick()" :loading="registerLoading" />
                    <div class="flex justify-content-center mt-3">
                        <Button label="Back to login" text @click="toggleRegister(false)" />
                    </div>
                    <transition-group name="p-message" tag="div">
                        <Message v-for="msg of message" :severity="msg.severity" :key="msg.content" :closable="false">{{ msg.content }}</Message>
                    </transition-group>
                </div>
            </div>
        </Transition>

    </div>
</template>

<style scoped></style>
