<script setup>

import { ref, computed, onMounted, onBeforeUnmount, inject } from 'vue';
import { useLayout } from '@/layout/composables/layout';

const $cookies = inject('$cookies');

const { changeTheme, setScale, layoutConfig, onMenuToggle } = useLayout();

const outsideClickListener = ref(null);
const topbarMenuActive = ref(false);

const scales = ref([12, 13, 14, 15, 16]);
const visible = ref(false);

var themeSetting = $cookies.get('onseidb_theme');

defineProps({
    simple: {
        type: Boolean,
        default: false
    }
});

onMounted(() => {
    bindOutsideClickListener();
});

onBeforeUnmount(() => {
    unbindOutsideClickListener();
});

const onConfigButtonClick = () => {
    visible.value = !visible.value;
};

const onChangeTheme = (theme, color, dark = undefined) => {
    changeTheme(theme, color, dark);
    themeSetting.theme = theme ? theme : themeSetting.theme;
    themeSetting.color = color ? color : themeSetting.color;
    if (dark !== undefined) {
        themeSetting.dark = dark;
    }
    $cookies.set('onseidb_theme', themeSetting);
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

// onChangeTheme(themeSetting.theme, themeSetting.color, themeSetting.dark);

</script>

<template>

    <div class="layout-topbar">
        <router-link to="/" class="layout-topbar-logo">
            <img :src="'onseidb-logo.svg'" alt="logo" />
            <span>OnseiDB</span>
        </router-link>

        <button class="p-link layout-menu-button layout-topbar-button" @click="onMenuToggle()">
            <i class="pi pi-bars"></i>
        </button>

        <!-- <button class="p-link layout-topbar-menu-button layout-topbar-button" @click="onTopBarMenuButton()">
            <i class="pi pi-ellipsis-v"></i>
        </button> -->

        <div class="layout-topbar-menu" :class="topbarMenuClasses">
            <!-- <button @click="onTopBarMenuButton()" class="p-link layout-topbar-button">
                <i class="pi pi-calendar"></i>
                <span>Calendar</span>
            </button>
            <button @click="onTopBarMenuButton()" class="p-link layout-topbar-button">
                <i class="pi pi-user"></i>
                <span>Profile</span>
            </button> -->
            <button @click="onConfigButtonClick()" class="p-link layout-topbar-button">
                <i class="fa-solid fa-palette"></i>
                <span>Theme</span>
            </button>
        </div>
    </div>

    <Sidebar v-model:visible="visible" position="right" :transitionOptions="'.3s cubic-bezier(0, 0, 0.2, 1)'" class="layout-config-sidebar w-20rem">
        <h5>Scale</h5>
        <div class="flex align-items-center">
            <Button icon="pi pi-minus" type="button" @click="decrementScale()" class="p-button-text p-button-rounded w-2rem h-2rem mr-2" :disabled="layoutConfig.scale.value === scales[0]"></Button>
            <div class="flex gap-2 align-items-center">
                <i class="pi pi-circle-fill text-300" v-for="s in scales" :key="s" :class="{ 'text-primary-500': s === layoutConfig.scale.value }"></i>
            </div>
            <Button icon="pi pi-plus" type="button" pButton @click="incrementScale()" class="p-button-text p-button-rounded w-2rem h-2rem ml-2" :disabled="layoutConfig.scale.value === scales[scales.length - 1]"></Button>
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

            <h5>Dark Theme</h5>
            <InputSwitch v-model="layoutConfig.darkTheme.value" @input="onChangeTheme(undefined, undefined, layoutConfig.darkTheme.value)" inputId="dark"></InputSwitch>

        <h5>Bootstrap</h5>
        <div class="grid">
            <div class="col-3">
                <button class="p-link w-2rem h-2rem" @click="onChangeTheme('bootstrap4', 'blue')">
                    <img src="/layout/images/themes/bootstrap4-light-blue.svg" class="w-2rem h-2rem" alt="Bootstrap Light Blue" />
                </button>
            </div>
            <div class="col-3">
                <button class="p-link w-2rem h-2rem" @click="onChangeTheme('bootstrap4', 'purple')">
                    <img src="/layout/images/themes/bootstrap4-light-purple.svg" class="w-2rem h-2rem" alt="Bootstrap Light Purple" />
                </button>
            </div>
        </div>

        <h5>Lara</h5>
        <div class="grid">
            <div class="col-3">
                <button class="p-link w-2rem h-2rem" @click="onChangeTheme('lara', 'blue')">
                    <img src="/layout/images/themes/lara-light-blue.png" class="w-2rem h-2rem" alt="Lara Light Blue" />
                </button>
            </div>
            <div class="col-3">
                <button class="p-link w-2rem h-2rem" @click="onChangeTheme('lara', 'teal')">
                    <img src="/layout/images/themes/lara-light-teal.png" class="w-2rem h-2rem" alt="Lara Light Teal" />
                </button>
            </div>
        </div>
    </Sidebar>

</template>

<style lang="scss" scoped></style>
