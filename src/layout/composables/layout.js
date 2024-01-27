import { toRefs, reactive, computed } from 'vue';

const layoutConfig = reactive({
    ripple: true,
    darkTheme: false,
    inputStyle: 'outlined',
    menuMode: 'static',
    theme: 'aura',
    color: 'blue',
    scale: 14,
    activeMenuItem: null
});

const layoutState = reactive({
    staticMenuDesktopInactive: false,
    overlayMenuActive: false,
    profileSidebarVisible: false,
    configSidebarVisible: false,
    staticMenuMobileActive: false,
    menuHoverActive: false
});

export function useLayout() {
    const changeTheme = (newThemeUrl) => {
        const elementId = 'theme-css';
        const linkElement = document.getElementById(elementId);
        const cloneLinkElement = linkElement.cloneNode(true);
        const themeUrl = linkElement.getAttribute('href');
        if (themeUrl.localeCompare(newThemeUrl) === 0) {
            return;
        }

        cloneLinkElement.setAttribute('id', elementId + '-clone');
        cloneLinkElement.setAttribute('href', newThemeUrl);
        cloneLinkElement.addEventListener('load', () => {
            linkElement.remove();
            cloneLinkElement.setAttribute('id', elementId);
        });
        linkElement.parentNode.insertBefore(cloneLinkElement, linkElement.nextSibling);
    };

    const changeColor = (theme, color) => {
        const dark = layoutConfig.darkTheme;
        const style = dark ? 'dark' : 'light';
        const newThemeUrl = `/themes/${theme}-${style}-${color}/theme.css`;

        changeTheme(newThemeUrl)
    }

    const darkToggle = () => {
        const theme = layoutConfig.theme;
        const color = layoutConfig.color;
        const dark = !layoutConfig.darkTheme;
        const style = dark ? 'dark' : 'light';
        const newThemeUrl = `/themes/${theme}-${style}-${color}/theme.css`;

        changeTheme(newThemeUrl)
    }

    const setScale = (scale) => {
        layoutConfig.scale = scale;
    };

    const setActiveMenuItem = (item) => {
        layoutConfig.activeMenuItem = item.value || item;
    };

    const onMenuToggle = () => {
        if (layoutConfig.menuMode === 'overlay') {
            layoutState.overlayMenuActive = !layoutState.overlayMenuActive;
        }

        if (window.innerWidth > 1200) {
            layoutState.staticMenuDesktopInactive = !layoutState.staticMenuDesktopInactive;
        } else {
            layoutState.staticMenuMobileActive = !layoutState.staticMenuMobileActive;
        }
    };

    const isSidebarActive = computed(() => layoutState.overlayMenuActive || layoutState.staticMenuMobileActive);

    const isDarkTheme = computed(() => layoutConfig.darkTheme);

    return { layoutConfig: toRefs(layoutConfig), layoutState: toRefs(layoutState), changeColor, darkToggle, setScale, onMenuToggle, isSidebarActive, isDarkTheme, setActiveMenuItem };
}
