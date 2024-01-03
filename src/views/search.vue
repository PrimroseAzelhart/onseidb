<script setup>

import { ref, onMounted } from 'vue';
import axios from 'axios'
import { cvService, circleService } from '@/service/search.js'

const pre = ref('RJ');
const iCode = ref(null);
const iTitle = ref('');
const iCircle = ref('');
const sCircle = ref([]);
const aCircle = ref('');
const iCV = ref('');
const sCV = ref([]);
const aCV = ref('');

const results = ref([]);
const resultText = ref('No results found');
const tableVisible = ref(false);

const cvSearch = new cvService();
const circleSearch = new circleService();

axios.defaults.headers["Content-Type"] = "application/x-www-form-urlencoded";

onMounted(() => {
    cvSearch.getCV().then((name) => (aCV.value = name));
    circleSearch.getCircle().then((name) => (aCircle.value = name));
});

const codeLabel = [
    {label: 'RJ', command: () => {pre.value = 'RJ'}},
    {label: 'BJ', command: () => {pre.value = 'BJ'}},
    {label: 'VJ', command: () => {pre.value = 'VJ'}}
];

const cols = [
    {field: 'code', header: 'Code'},
    {field: 'title', header: 'Title'},
    {field: 'cv', header: 'CV'},
    {field: 'circle', header: 'Circle'}
]

const searchCircle = (event) => {
    setTimeout(() => {
        if(!event.query.trim().length) {
            sCircle.value = [...aCircle.value];
        } else {
            sCircle.value = aCircle.value.filter((name) => {
                return name.toLowerCase().includes(event.query.toLowerCase());
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
                return name.toLowerCase().includes(event.query.toLowerCase());
            })
        }
    }, 250)
};

const onSubmit = () => {
    axios.post('http://api.onsei.fans/search', {
            option: 'code'
        })
        .then(function (response) {
            console.log(response.data.list);
            results.value = response.data.list;
            const count = response.data.list.length
            if (count === 0) {
                resultText.value = 'No results found';
            } else {
                resultText.value = `Found ${count} result(s)`;
            }
        })
        .catch(function (error) {
            console.log(error);
        });
};

</script>

<template>
    <div class="card">
        <Panel header="Search Options" toggleable>

            <div class="grid p-fluid">

                <div class="field col-12 md:col-4">
                    <label for="wcode">Code</label>
                    <div class="p-inputgroup">
                        <SplitButton :label="pre" :model="codeLabel"></SplitButton>
                        <InputMask type="text" id="wcode" v-model="iCode" mask="99999999" slotChar="" placeholder="Number only" />
                    </div>
                </div>

                <div class="field col-12 md:col-4">
                    <label for="title">Title</label>
                    <InputText type="text" id="title" v-model="iTitle" />
                </div>

                <div class="field col-12 md:col-4">
                    <label for="circle">Circle</label>
                    <AutoComplete type="text" inputId="circle" v-model="iCircle" :suggestions="sCircle" dropdown @complete="searchCircle" />
                </div>

                <div class="field col-12 ">
                    <label for="cv">CV</label>
                    <AutoComplete type="text" inputId="cv" v-model="iCV" :suggestions="sCV" :multiple="true" dropdown @complete="searchCV" />
                </div>

            </div>
            <br />
            <div class="flex justify-content-end">
                <Button label="Submit" @click="onSubmit"></Button>
            </div>

        </Panel>
    </div>

    <div class="card">
        <Panel header="Search Results" toggleable>
            {{ resultText }}
            <DataTable :value="results" v-model:visible="tableVisible">
                <Column v-for="col of cols" :key="col.field" :field="col.field" :header="col.header"></Column>
            </DataTable>
        </Panel>
    </div>

</template>

<style lang="scss">

.p-tieredmenu {
    width: auto;
}

.p-autocomplete-empty-message {
    padding: 0rem 1rem;
}

</style>
