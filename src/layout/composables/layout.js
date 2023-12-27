import { toRefs, reactive, computed } from 'vue';

const layoutConfig = reactive({
    ripple: false,
    darkTheme: false,
    inputStyle: 'outlined',
    menuMode: 'static',
    theme: 'bootstrap4',
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
    const changeTheme = (theme, color, dark) => {
        const elementId = 'theme-css';
        const linkElement = document.getElementById(elementId);
        const cloneLinkElement = linkElement.cloneNode(true);
        const themeUrl = linkElement.getAttribute('href');
        var newThemeUrl = '';

        theme = theme ? theme : layoutConfig.theme;
        color = color ? color : layoutConfig.color;
        dark = (dark !== undefined) ? dark : layoutConfig.darkTheme;
        const style = dark ? 'dark' : 'light';
        newThemeUrl = `/themes/${theme}-${style}-${color}/theme.css`;

        if (themeUrl.localeCompare(newThemeUrl) === 0) {
            return;
        }

        layoutConfig.theme = theme;
        layoutConfig.color = color;
        layoutConfig.darkTheme = dark;

        cloneLinkElement.setAttribute('id', elementId + '-clone');
        cloneLinkElement.setAttribute('href', newThemeUrl);
        cloneLinkElement.addEventListener('load', () => {
            linkElement.remove();
            cloneLinkElement.setAttribute('id', elementId);
        });
        linkElement.parentNode.insertBefore(cloneLinkElement, linkElement.nextSibling);
    };

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

        if (window.innerWidth > 991) {
            layoutState.staticMenuDesktopInactive = !layoutState.staticMenuDesktopInactive;
        } else {
            layoutState.staticMenuMobileActive = !layoutState.staticMenuMobileActive;
        }
    };

    const isSidebarActive = computed(() => layoutState.overlayMenuActive || layoutState.staticMenuMobileActive);

    const isDarkTheme = computed(() => layoutConfig.darkTheme);

    return { layoutConfig: toRefs(layoutConfig), layoutState: toRefs(layoutState), changeTheme, setScale, onMenuToggle, isSidebarActive, isDarkTheme, setActiveMenuItem };
}
