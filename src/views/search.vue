<script setup>

import { ref, onMounted } from 'vue';
import { cvService, circleService } from '@/service/search.js'

const iRJ = ref('');
const iTitle = ref('');
const iCircle = ref('');
const sCircle = ref([]);
const aCircle = ref('');
const iCV = ref('');
const sCV = ref([]);
const aCV = ref('');

const cvSearch = new cvService();
const circleSearch = new circleService();

onMounted(() => {
    cvSearch.getCV().then((name) => (aCV.value = name));
    circleSearch.getCircle().then((name) => (aCircle.value = name));
})

const searchCircle = (event) => {
    setTimeout(() => {
        if(!event.query.trim().length) {
            sCircle.value = [...aCircle.value];
        } else {
            sCircle.value = aCircle.value.filter((name) => {
                return name.includes(event.query);
            })
        }
    }, 250)
};

const searchCV = (event) => {
    setTimeout(() => {
        if(!event.query.trim().length) {
            sCV.value = [...aCV.value];
        } else {
            sCV.value = aCV.value.filter((name) => {
                return name.includes(event.query);
            })
        }
    }, 250)
};

</script>

<template>
<Panel header="Search Options" toggleable>

        <div class="grid p-fluid">

            <div class="field col-12 md:col-4">
                <label for="rj">RJ</label>
                <InputText type="text" id="rj" v-model="iRJ" v-tooltip.bottom="'Either numeric or with RJ is OK'" />
            </div>

            <div class="field col-12 md:col-4">
                <label for="title">Title</label>
                <InputText type="text" id="title" v-model="iTitle" />
            </div>

            <div class="field col-12 md:col-4">
                <label for="circle">Circle</label>
                <AutoComplete type="text" inputId="circle" v-model="iCircle" :suggestions="sCircle" dropdown @complete="searchCircle" />
            </div>

            <div class="field col-12">
                <label for="cv">CV</label>
                <AutoComplete type="text" inputId="cv" v-model="iCV" :suggestions="sCV" :multiple="true" dropdown @complete="searchCV" />
            </div>

        </div>

</Panel>
</template>
