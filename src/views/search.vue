<script setup>

import { ref, onMounted, isRuntimeOnly } from 'vue';
import { useToast } from 'primevue/usetoast';
import axios from 'axios'
import { cvService, circleService, tagService } from '@/service/search.js'

const pre = ref('RJ');
const iCode = ref(null);
const iTitle = ref(null);
const iCircle = ref(null);
const sCircle = ref(null);
const aCircle = ref(null);
const iCV = ref(null);
const sCV = ref(null);
const iAge = ref([]);

const releaseDate = ref(null);
const releaseAfter = ref(null);
const releaseBefore = ref(null);
const releaseDateDisable = ref(false);
const releasePeriodDisable = ref(false);
const iTags = ref(null);
const sTags = ref(null);

const inputGroup = [iCode, iTitle, iCircle, iCV, iAge, releaseDate, releaseAfter, releaseBefore, iTags]

const results = ref([]);
const advOptions = ref(false);
const worksPerPage = ref(10);

const submitLoading = ref(false);

const sortKey = ref();
const sortAscend = ref(false);

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

const sortOptions = ref([
    {label: 'Release date', value: 'date'},
    {label: 'Price', value: 'price'},
]);

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

const ageButtonToggle = (value) => {
    if (iAge.value.includes(value)) {
        iAge.value.splice(iAge.value.indexOf(value), 1);
    } else {
        iAge.value.push(value);
    }
}

const ageStyle = (value) => {
    return iAge.value.includes(value);
}

const onClear = () => {
    inputGroup.forEach(item => {
        item.value = null;
    });
    iAge.value = [];
};

const responseError = (code, message) => {
    toast.add({ severity: 'error', summary: `${code}`, detail: `${message}`, life: 5000 });
};

const onSubmit = () => {
    submitLoading.value = true;
    axios.post('http://api.onsei.fans/search', {
            option: 'code'
        })
        .then(function (response) {
            results.value = response.data.list;
            // const count = response.data.list.length
            results.value.forEach((item) => {
                item.year = parseInt(item.date / 10000);
                item.month = parseInt(item.date % 10000 / 100);
                item.day = item.date % 100;
            });
            sortResults();
            submitLoading.value = false;
            console.log(results.value);
        })
        .catch(function (error) {
            console.log(error);
            responseError(error.code, error.message);
            submitLoading.value = false;
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

const compareResults = (a, b) => {
    return (sortAscend.value ? (a-b) : (b-a));
}

const sortFunc = (a, b) => {
    var res = 0;
    switch (sortKey.value) {
        case 'price':
            res = compareResults(a.price, b.price);
            break;
        case 'date':
            res = compareResults(a.date, b.date);
            break;
        default:
            res = 0;
    }
    return res;
}

const sortResults = (toggle) => {
    if (toggle) {
        sortAscend.value = !sortAscend.value;
    }
    results.value.sort(sortFunc);
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
                        <SplitButton :label="pre" :model="codeLabel" />
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
                        <span class="p-buttonset">
                            <Button v-for="item in ageOpts" :label="item.option" @click="ageButtonToggle(item.value)" :text="!ageStyle(item.value)"
                                :icon="ageStyle(item.value)?'fa-regular fa-square-check fa-lg':'fa-regular fa-square fa-lg'" />
                        </span>
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
                            @click="onClear" class="w-max" />
                        <Button label="Submit" icon="fa-regular fa-circle-check fa-xl" iconPos="right"
                            @click="onSubmit" class="w-max" :loading="submitLoading" />
                    </div>
                </div>

            </div>
        </Panel>
    </div>

    <div class="card">
        <Panel header="Search Results" toggleable>
            <!-- <DataView :value="results" paginator :rows="worksPerPage" :sortOrder="sortAscend?-1:1" :sortField="sortField"> -->
            <DataView :value="results" paginator :rows="worksPerPage">
                <template #header>
                    <div class="flex gap-3">
                        <Dropdown v-model="sortKey" :options="sortOptions" optionLabel="label" optionValue="value"
                            @change="sortResults" placeholder="Sort by..." class="w-12rem" />
                        <Button @click="sortResults(true)" rounded
                            :icon="sortAscend?'fa-solid fa-arrow-up-wide-short':'fa-solid fa-arrow-down-wide-short'" />
                    </div>
                </template>
                <template #list="slotProps">
                    <div class="col-12">
                        <div class="flex flex-row align-items-center justify-content-start p-3 gap-3 w-full h-10rem">
                            <Image src="onseidb-logo.svg" alt="Image" preview />
                            <div class="flex flex-row justify-content-between align-items-start w-full h-full gap-3">
                                <div class="flex flex-column justify-content-between h-full flex-grow-1 w-1rem">
                                    <div class="text-2xl font-bold text-900 text-overflow-ellipsis overflow-hidden white-space-nowrap">{{ slotProps.data.title }}</div>
                                    <div class="white-space-nowrap">{{ slotProps.data.circle }}</div>
                                    <div>{{ slotProps.data.cv }}</div>
                                    <div class="flex gap-2">
                                        <Tag v-for="item in slotProps.data.tag" :value="item" rounded />
                                    </div>
                                </div>
                                <div class="flex flex-column justify-content-between align-items-end h-full min-w-max">
                                    <div class="text-2xl font-semibold">￥{{ slotProps.data.price }}</div>
                                    <div>{{ slotProps.data.year }}-{{ slotProps.data.month }}-{{ slotProps.data.day }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </template>
            </DataView>
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

.p-paginator {
    border-width: 0rem;
}

</style>
