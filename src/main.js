import { createApp } from 'vue'

import App from './App.vue'
import router from '@/router'

import '@/assets/styles.scss'
import PrimeVue from 'primevue/config'

const app = createApp(App)

app.use(PrimeVue, {ripple: true})
app.use(router)
app.mount('#app')
