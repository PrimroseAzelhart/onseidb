<script setup>

import { ref, computed, onMounted, onBeforeUnmount, reactive } from 'vue';
import { useLayout } from '@/layout/composables/layout';

import Sidebar from 'primevue/sidebar';
import { usePrimeVue } from 'primevue/config';

import { useOverlayScrollbars } from "overlayscrollbars-vue";

import router from '@/router';

const PrimeVue = usePrimeVue();
const { setScale, layoutConfig, onMenuToggle } = useLayout();

const outsideClickListener = ref(null);
const topbarMenuActive = ref(false);

const scales = ref([12, 13, 14, 15, 16]);
const visible = ref(false);
const themeDark = ref(false);
const themeColor = ref('blue');

const colors = ['blue', 'teal'];

defineProps({
    simple: {
        type: Boolean,
        default: false
    }
});

const scrollbarOption = reactive({
    scrollbars: {
        theme: 'os-theme-dark'
    }
});

onMounted(() => {
    bindOutsideClickListener();
    initOverlayScrollbars(document.body);

    const localTheme = localStorage.getItem('theme');
    if (localTheme) {
        const themeSetting = JSON.parse(localTheme);
        themeDark.value = themeSetting['dark'];
        themeColor.value = themeSetting['color'];
        const style = themeDark.value ? 'dark' : 'light';
        scrollbarOption.scrollbars.theme = themeDark.value ? 'os-theme-light' : 'os-theme-dark';
        PrimeVue.changeTheme('aura-light-blue', `aura-${style}-${themeColor.value}`, 'theme-css', () => {});
    }
});

onBeforeUnmount(() => {
    unbindOutsideClickListener();
});

const onLogoutButtonClick = () => {
    router.push('/logout');
}

const onConfigButtonClick = () => {
    visible.value = !visible.value;
};

const onTopBarMenuButton = () => {
    topbarMenuActive.value = !topbarMenuActive.value;
};

const decrementScale = () => {
    setScale(layoutConfig.scale.value - 1);
    applyScale();
};

const incrementScale = () => {
    setScale(layoutConfig.scale.value + 1);
    applyScale();
};

const applyScale = () => {
    document.documentElement.style.fontSize = layoutConfig.scale.value + 'px';
};

const topbarMenuClasses = computed(() => {
    return {
        'layout-topbar-menu-mobile-active': topbarMenuActive.value
    };
});

const bindOutsideClickListener = () => {
    if (!outsideClickListener.value) {
        outsideClickListener.value = (event) => {
            if (isOutsideClicked(event)) {
                topbarMenuActive.value = false;
            }
        };
        document.addEventListener('click', outsideClickListener.value);
    }
};

const unbindOutsideClickListener = () => {
    if (outsideClickListener.value) {
        document.removeEventListener('click', outsideClickListener);
        outsideClickListener.value = null;
    }
};

const isOutsideClicked = (event) => {
    if (!topbarMenuActive.value) return;

    const sidebarEl = document.querySelector('.layout-topbar-menu');
    const topbarEl = document.querySelector('.layout-topbar-menu-button');

    return !(sidebarEl.isSameNode(event.target) || sidebarEl.contains(event.target) || topbarEl.isSameNode(event.target) || topbarEl.contains(event.target));
};

const onChangeColor = (color) => {
    const style = themeDark.value ? 'dark' : 'light';
    const oldTheme = `aura-${style}-${themeColor.value}`;
    const newTheme = `aura-${style}-${color}`;
    PrimeVue.changeTheme(oldTheme, newTheme, 'theme-css', () => {});
    themeColor.value = color;
    localStorage.setItem('theme', JSON.stringify({'color': color, 'dark': themeDark.value}));
};

const onDarkToggle = () => {
    scrollbarOption.scrollbars.theme = themeDark.value ? 'os-theme-dark' : 'os-theme-light';
    const oldStyle = themeDark.value ? 'dark' : 'light';
    const newStyle = themeDark.value ? 'light' : 'dark';
    const oldTheme = `aura-${oldStyle}-${themeColor.value}`;
    const newTheme = `aura-${newStyle}-${themeColor.value}`;
    PrimeVue.changeTheme(oldTheme, newTheme, 'theme-css', () => {});
    localStorage.setItem('theme', JSON.stringify({'color': themeColor.value, 'dark': !themeDark.value}));
};

const [initOverlayScrollbars] = useOverlayScrollbars({defer: true, options: scrollbarOption});

</script>

<template>
    <div class="layout-topbar">
        <router-link to="/" class="layout-topbar-logo">
            <!-- <img :src="'onseidb-logo.svg'" alt="logo" class="logo"/> -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <g fill="currentColor">
                    <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3"/>
                    <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7"/>
                    <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3s7 1.343 7 3"/>
                </g>
            </svg>
            <span>OnseiDB</span>
        </router-link>

        <button class="p-link layout-menu-button layout-topbar-button" @click="onMenuToggle()">
            <i class="fa-solid fa-bars"></i>
        </button>

        <button class="p-link layout-topbar-menu-button layout-topbar-button" @click="onTopBarMenuButton()">
            <i class="fa-solid fa-ellipsis"></i>
        </button>

        <div class="layout-topbar-menu" :class="topbarMenuClasses">
            <button @click="onLogoutButtonClick()" class="p-link layout-topbar-button">
                <i class="fa-solid fa-right-from-bracket"></i>
                <span>Logout</span>
            </button>
            <button @click="onConfigButtonClick()" class="p-link layout-topbar-button">
                <i class="fa-solid fa-gear"></i>
                <span>Settings</span>
            </button>
        </div>
    </div>

    <Sidebar v-model:visible="visible" position="right" :transitionOptions="'.3s cubic-bezier(0, 0, 0.2, 1)'" class="layout-config-sidebar w-20rem">
        <h5>Scale</h5>
        <div class="flex align-items-center">
            <Button icon="fa-solid fa-minus fa-lg" type="button" @click="decrementScale()" class="p-button-text p-button-rounded w-2rem h-2rem mr-2" :disabled="layoutConfig.scale.value === scales[0]"></Button>
            <div class="flex gap-2 align-items-center">
                <i class="fa-regular fa-circle fa-lg text-300" v-for="s in scales" :key="s" :class="{ 'text-primary-500': s === layoutConfig.scale.value }"></i>
            </div>
            <Button icon="fa-solid fa-plus fa-lg" type="button" pButton @click="incrementScale()" class="p-button-text p-button-rounded w-2rem h-2rem ml-2" :disabled="layoutConfig.scale.value === scales[scales.length - 1]"></Button>
        </div>

        <h5>Menu Type</h5>
        <div class="flex">
            <div class="field-radiobutton flex-1">
                <RadioButton name="menuMode" value="static" v-model="layoutConfig.menuMode.value" inputId="mode1"></RadioButton>
                <label for="mode1">Static</label>
            </div>
            <div class="field-radiobutton flex-1">
                <RadioButton name="menuMode" value="overlay" v-model="layoutConfig.menuMode.value" inputId="mode2"></RadioButton>
                <label for="mode2">Overlay</label>
            </div>
        </div>

        <h5>Dark Mode</h5>
        <InputSwitch v-model="themeDark" @input="onDarkToggle()" inputId="dark"></InputSwitch>

        <h5>Color</h5>
        <div class="grid">
            <!-- <div v-for="color in colors" class="col-3">
                <Button v-if="color === themeColor"><i class="fa-solid fa-check"></i></Button>
                <Button v-else icon="NULL"></Button>
            </div> -->
            <div class="col-3">
                <button class="p-link w-2rem h-2rem" @click="onChangeColor('blue')">
                    <img src="/layout/images/themes/lara-light-blue.png" class="w-2rem h-2rem" alt="Aura Blue" />
                </button>
            </div>
            <div class="col-3">
                <button class="p-link w-2rem h-2rem" @click="onChangeColor('teal')">
                    <img src="/layout/images/themes/lara-light-teal.png" class="w-2rem h-2rem" alt="Aura Teal" />
                </button>
            </div>
        </div>
    </Sidebar>
</template>

<style lang="scss" scoped></style>
