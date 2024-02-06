import { createApp } from 'vue'

import App from './App.vue'

import Button from 'primevue/button';
import Card from 'primevue/card';
import Chip from 'primevue/chip';
import Dropdown from 'primevue/dropdown';
import Image from 'primevue/image';
import InputSwitch from 'primevue/inputswitch';
import InputText from 'primevue/inputtext';
import InputMask from 'primevue/inputmask';
import Message from 'primevue/message';
import MultiSelect from 'primevue/multiselect';
import Panel from 'primevue/panel';
import RadioButton from 'primevue/radiobutton';
import SelectButton from 'primevue/selectbutton';
import SplitButton from 'primevue/splitbutton';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';
import Toolbar from 'primevue/toolbar';
import Tag from 'primevue/tag';
import PrimeVue from 'primevue/config'

import VueCookies from "vue-cookies";
import router from '@/router'
import '@/assets/styles.scss'
// import '../main.css'
import 'overlayscrollbars/styles/overlayscrollbars.css';

const app = createApp(App)

app.use(PrimeVue, {ripple: true});
app.use(ToastService);

app.use(VueCookies);
app.use(router);

app.component('Button', Button);
app.component('Card', Card);
app.component('Chip', Chip);
app.component('Dropdown', Dropdown);
app.component('Image', Image);
app.component('InputMask', InputMask);
app.component('InputSwitch', InputSwitch);
app.component('InputText', InputText);
app.component('Message', Message);
app.component('MultiSelect', MultiSelect);
app.component('Panel', Panel);
app.component('RadioButton', RadioButton);
app.component('SelectButton', SelectButton);
app.component('SplitButton', SplitButton);
app.component('Tag', Tag);
app.component('Toast', Toast);
app.component('Toolbar', Toolbar);

app.mount('#app')
