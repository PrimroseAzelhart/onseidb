import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { visualizer } from "rollup-plugin-visualizer";

import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@' : path.resolve(__dirname, './src')
    },
  },
  build: {
    rollupOptions: {
      plugins: [visualizer({ open: true })],
    },
  },
  plugins: [vue()]
})
