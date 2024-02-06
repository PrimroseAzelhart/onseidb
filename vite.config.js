import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { visualizer } from "rollup-plugin-visualizer";
import {browserslistToTargets} from 'lightningcss';

import path from 'path'
import browserslist from 'browserslist';

// https://vitejs.dev/config/
export default defineConfig({
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src')
        },
    },
    // css: {
    //     transformer: 'lightningcss',
    //     lightningcss: {
    //         targets: browserslistToTargets(browserslist('>= 0.25%'))
    //     }
    // },
    build: {
        // cssMinify: 'lightningcss',
        rollupOptions: {
            plugins: [visualizer({ open: true })],
        },
    },
    plugins: [vue()]
})
