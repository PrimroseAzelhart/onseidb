<script setup>

import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';
import axios from 'axios'
import { cvService, circleService, tagService } from '@/service/search.js'

const pre = ref('RJ');
const iCode = ref(null);
const iTitle = ref('');
const iCircle = ref('');
const sCircle = ref([]);
const aCircle = ref([]);
const iCV = ref([]);
const sCV = ref([]);
const iAge = ref([]);

const releaseDate = ref(null);
const releaseAfter = ref(null);
const releaseBefore = ref(null);
const releaseDateDisable = ref(false);
const releasePeriodDisable = ref(false);
const iTags = ref([]);
const sTags = ref([]);

const results = ref([]);
const resultText = ref('No results found');
const advOptions = ref(true);

const cvSearch = new cvService();
const circleSearch = new circleService();
const tagSearch = new tagService();

const toast = useToast();

axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded';

onMounted(() => {
    cvSearch.getCV().then((name) => (sCV.value = name));
    circleSearch.getCircle().then((name) => (aCircle.value = name));
    tagSearch.getTag().then((tags) => (sTags.value = tags));
});

const codeLabel = [
    {label: 'RJ', command: () => {pre.value = 'RJ'}},
    {label: 'BJ', command: () => {pre.value = 'BJ'}},
    {label: 'VJ', command: () => {pre.value = 'VJ'}}
];

const ageOpts = ref([
    { option: 'A', value: 1 },
    { option: 'B', value: 2 },
    { option: 'C', value: 3 }
]);

const cols = [
    {field: 'code', header: 'Code'},
    {field: 'title', header: 'Title'},
    {field: 'cv', header: 'CV'},
    {field: 'circle', header: 'Circle'}
]

const tagsPanelOpts = {
    itemSize: 40
}

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

const responseError = (code, message) => {
    toast.add({ severity: 'error', summary: `${code}`, detail: `${message}`, life: 5000 });
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
            responseError(error.code, error.message);
        });
};

// Toggle extra options
const onAdvOpt = () => {
    advOptions.value = !advOptions.value;
};

const onReleaseDateInput = (value) => {
    releasePeriodDisable.value = value === null ? false : true;
}

const onReleasePeriodInput = (value) => {
    releaseDateDisable.value = value === null ? false : true;
}

const debug = (value) => {
    console.log(value);
}

</script>

<template>
    <div class="card">
        <Panel header="Search Options" toggleable>

            <div class="grid p-fluid">

                <div class="field col-12 md:col-4">
                    <label for="wcode">Code</label>
                    <div class="p-inputgroup">
                        <SplitButton :label="pre" :model="codeLabel"></SplitButton>
                        <InputMask type="text" id="wcode" v-model="iCode" mask="99999999"
                            slotChar="" placeholder="Number only" />
                    </div>
                </div>

                <div class="field col-12 md:col-4">
                    <label for="title">Title</label>
                    <InputText type="text" id="title" v-model="iTitle" placeholder="Input title"/>
                </div>

                <div class="field col-12 md:col-4">
                    <label for="circle">Circle</label>
                    <AutoComplete type="text" inputId="circle" placeholder="Select circle"
                        v-model="iCircle" :suggestions="sCircle"
                        dropdown forceSelection @complete="searchCircle" />
                </div>

                <div class="field col-12 md:col-6">
                    <label for="cv">CV</label>
                    <MultiSelect inputId="cv" placeholder="Select CV" v-model="iCV" showToggleAll
                        :options="sCV" display="chip" filter :selectionLimit="3"
                        :virtualScrollerOptions="tagsPanelOpts" @update:modelValue="">
                    </MultiSelect>
                </div>
                <div class="field col-12 md:col-6">
                    <label>Age</label>
                        <SelectButton v-model="iAge" :options="ageOpts"
                            optionLabel="option" optionValue="value" multiple />
                </div>

                <template v-if="advOptions">
                    <div class="field col-12 md:col-4">
                        <label for="rDate">Release Date</label>
                        <Calendar showIcon showButtonBar inputId="rDate" v-model="releaseDate"
                            @update:modelValue="onReleaseDateInput" :disabled="releaseDateDisable" />
                    </div>
                    <div class="field col-12 md:col-4">
                        <label for="rAfter">Release After</label>
                        <Calendar showIcon showButtonBar inputId="rAfter" v-model="releaseAfter"
                            @update:modelValue="onReleasePeriodInput" :disabled="releasePeriodDisable" />
                    </div>
                    <div class="field col-12 md:col-4">
                        <label for="rBefore">Release Before</label>
                        <Calendar showIcon showButtonBar inputId="rBefore" v-model="releaseBefore"
                            @update:modelValue="onReleasePeriodInput" :disabled="releasePeriodDisable" />
                    </div>

                    <div class="field col-12">
                        <label for="tags">Tags</label>
                        <MultiSelect inputId="tags" placeholder="Select tag" v-model="iTags" showToggleAll
                            filter :options="sTags" display="chip" optionLabel="label" optionValue="code"
                            :virtualScrollerOptions="tagsPanelOpts" :selectionLimit="5">
                        </MultiSelect>
                    </div>

                    <div class="field col-12 md:col-4">
                        <label for="series">Series</label>
                        <AutoComplete type="text" inputId="series" placeholder="Select series"
                            v-model="iCircle" :suggestions="sCircle"
                            dropdown forceSelection @complete="searchCircle" />
                    </div>
                    <div class="field col-12 md:col-4">
                        <label for="author">Author</label>
                        <AutoComplete type="text" inputId="author" placeholder="Select author"
                            v-model="iCircle" :suggestions="sCircle"
                            dropdown forceSelection @complete="searchCircle" />
                    </div>
                    <div class="field col-12 md:col-4">
                        <label for="illustrator">Illustrator</label>
                        <AutoComplete type="text" inputId="illustrator" placeholder="Select illustrator"
                            v-model="iCircle" :suggestions="sCircle"
                            dropdown forceSelection @complete="searchCircle" />
                    </div>
                </template>

                <div class="field col-12 md:col-6">
                    <div class="flex md:justify-content-start">
                        <Button label="Advanced Options" @click="onAdvOpt" class="md:w-max" iconPos="right"
                            :icon="advOptions?'fa-solid fa-angles-up fa-xl':'fa-solid fa-angles-down fa-xl'" />
                    </div>
                </div>
                <div class="field col-12 md:col-6">
                    <Toast />
                    <div class="flex justify-content-between md:justify-content-end gap-3">
                        <Button label="Clear" icon="fa-regular fa-circle-xmark fa-xl" iconPos="right"
                            class="w-max" />
                        <Button label="Submit" icon="fa-regular fa-circle-check fa-xl" iconPos="right"
                            @click="onSubmit" class="w-max" />
                    </div>
                </div>

            </div>

        </Panel>
    </div>

    <div class="card">
        <Panel header="Search Results" toggleable>
            <DataTable :value="results" tableStyle="min-width: 60rem">
                <template #header> {{ resultText }} </template>
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

.field {
    margin-bottom: 0.5rem;
}

</style>
