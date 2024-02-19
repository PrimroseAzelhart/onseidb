<script setup>

import { ref, onMounted, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import axios from 'axios'
import { databaseService } from '@/service/api.js'

import AutoComplete from 'primevue/autocomplete';
import Calendar from 'primevue/calendar';
import DataView from 'primevue/dataview';
import DataViewLayoutOptions  from 'primevue/dataviewlayoutoptions'

import WorkListLayoutItem from '@/components/WorkListLayoutItem.vue'
import WorkGridLayoutItem from '@/components/WorkGridLayoutItem.vue'

const pre = ref('RJ');
const iD = ref(null);
const iTitle = ref(null);
const iCircle = ref(null);
const sCircle = ref(null);
const aCircle = ref(null);
const iCV = ref(null);
const sCV = ref(null);
const iAge = ref([]);

const releaseDate = ref([]);
const iGenres = ref(null);
const sGenres = ref(null);
const iSeries = ref(null);
const sSeries = ref(null);
const aSeries = ref(null);
const iScripter = ref(null);
const sScripter = ref(null);
const aScripter = ref(null);
const iIllustrator = ref(null);
const sIllustrator = ref(null);
const aIllustrator = ref(null);

const inputGroup = [iD, iTitle, iCircle, iCV, iAge, releaseDate, iGenres, iSeries, iScripter, iIllustrator];
const keyGroup = ['id', 'title', 'circle', 'cv', 'age', 'rel_date', 'genre', 'series', 'scripter', 'illustrator'];
const selectionGroup = [aCircle, sCV, sGenres, aSeries, aScripter, aIllustrator];
const selectionKey = ['circle', 'cv', 'genre', 'series', 'scripter', 'illustrator'];
const advOptions = ref(false);
const submitLoading = ref(false);

const results = ref([]);
const sortKey = ref('date');
const sortAscend = ref(false);
const resultsPerPage = ref(10);
const resultsShow = ref(true);
const resultsLayout = ref('list');
const detailShow = ref(false);
const detailID = ref('');
const detail = ref();

const db = new databaseService();

const toast = useToast();

const axiosInstance = axios.create({
    headers: {
        "Content-Type": 'application/x-www-form-urlencoded',
    }
});

onMounted(() => {
    for (var i = 0; i < selectionKey.length; i++) {
        const res = db.retrieve(selectionKey[i]);
        if (res) {
            selectionGroup[i].value = JSON.parse(res);
        }
    }
});

const idPre = ['RJ', 'BJ', 'VJ'];

const ageOpts = ref([
    { option: 'A', value: 0 },
    { option: 'B', value: 1 },
    { option: 'C', value: 2 }
]);

const sortOptions = ref([
    {label: 'Release date', value: 'date'},
    {label: 'Price', value: 'price_current'},
    {label: 'Sales', value: 'dl'}
]);

const tagsPanelOpts = {
    itemSize: 40
};

const resultsPerPageOpts = [10, 20, 50];

const sortOrderIcon = computed(() => {
    return sortAscend.value ? 'fa-solid fa-arrow-up-wide-short' : 'fa-solid fa-arrow-down-wide-short';
});

const ageIcon = (value) => {
    return ageChecked(value) ? 'fa-regular fa-square-check fa-lg' : 'fa-regular fa-square fa-lg';
};

const searchCircle = (event) => {
    setTimeout(() => {
        if(!event.query.trim().length) {
            sCircle.value = [...aCircle.value];
        } else {
            sCircle.value = aCircle.value.filter((name) => {
                return name.name.toLowerCase().includes(event.query.toLowerCase());
            })
        }
    }, 250);
};

const searchSeries = (event) => {
    setTimeout(() => {
        if(!event.query.trim().length) {
            sSeries.value = [...aSeries.value];
        } else {
            sSeries.value = aSeries.value.filter((name) => {
                return name.name.toLowerCase().includes(event.query.toLowerCase());
            })
        }
    }, 250);
};

const searchScripter = (event) => {
    setTimeout(() => {
        if(!event.query.trim().length) {
            sScripter.value = [...aScripter.value];
        } else {
            sScripter.value = aScripter.value.filter((name) => {
                return name.name.toLowerCase().includes(event.query.toLowerCase());
            })
        }
    }, 250);
};

const searchIllustrator = (event) => {
    setTimeout(() => {
        if(!event.query.trim().length) {
            sIllustrator.value = [...aIllustrator.value];
        } else {
            sIllustrator.value = aIllustrator.value.filter((name) => {
                return name.name.toLowerCase().includes(event.query.toLowerCase());
            })
        }
    }, 250);
};

const ageButtonToggle = (value) => {
    if (iAge.value.includes(value)) {
        iAge.value.splice(iAge.value.indexOf(value), 1);
    } else {
        iAge.value.push(value);
    }
};

const ageChecked = (value) => {
    return iAge.value.includes(value);
};

const onClear = () => {
    inputGroup.forEach(item => {
        item.value = null;
    });
    iAge.value = [];
    releaseDate.value = [];
};

const responseError = (code, message) => {
    toast.add({ severity: 'error', summary: `${code}`, detail: `${message}`, life: 5000 });
};

const isEmpty = (item) => {
    if (Array.isArray(item.value)) {
        return item.value.length === 0;
    } else {
        return !item.value;
    }
};

const postProcess = () => {
    results.value.forEach((item) => {
        const d = new Date(item.release_date);
        item.date = d.getTime() / 1000;
    });

    sortResults();
};

const generatePostData = () => {
    var data = {};
    if (iD.value) {
        data['id'] = pre.value + iD.value;
        return data;
    }
    // Adapt time zone
    releaseDate.value.forEach(item => {
        if (item) {
            const offset = item.getTimezoneOffset() / -60;
            item = item.setHours(item.getHours() + offset);
        }
    });
    for (var i = 1; i < keyGroup.length; i++) {
        if (Array.isArray(inputGroup[i].value)) {
            if (inputGroup[i].value !==0) {
                data[keyGroup[i]] = inputGroup[i].value;
            }
        } else {
            if (inputGroup[i].value) {
                data[keyGroup[i]] = inputGroup[i].value;
            }
        }
    }
    // console.log(data)
    return data;
};

const onSubmit = () => {
    if (inputGroup.every(isEmpty)) {
        responseError("Empty options", "Please fill at least 1 field");
        return;
    }
    submitLoading.value = true;
    axiosInstance.post('https://api.onsei.fans/query', generatePostData())
        .then((response) => {
            results.value = response.data;
            // const count = response.data.list.length
            postProcess();
            submitLoading.value = false;
            console.log(results.value);
            toggleDetail(false);
        })
        .catch((error) => {
            console.log(error);
            responseError(error.code, error.message);
            submitLoading.value = false;
        });
};

// Toggle extra options
const onAdvOpt = () => {
    advOptions.value = !advOptions.value;
};

const sortFunc = (a, b) => {
    const na = a[sortKey.value];
    const nb = b[sortKey.value];
    return (sortAscend.value ? (na-nb) : (nb-na));
};

const sortResults = (toggle) => {
    if (toggle) {
        sortAscend.value = !sortAscend.value;
    }
    results.value.sort(sortFunc);
};

const toggleDetail = (show) => {
    if (show) {
        resultsShow.value = false;
        setTimeout(() => {
            detailShow.value = true;
        }, 500);
    } else {
        detailShow.value = false;
        setTimeout(() => {
            resultsShow.value = true;
        }, 500);
    }
};

const onDetailClick = (id) => {
    detailID.value = id;
    toggleDetail(true);
};

const debug = (value) => {
    console.log(value);
};

</script>

<template>

    <div class="card">
        <Panel header="Search Options" toggleable>
            <div class="grid p-fluid">

                <div class="field col-12 md:col-4 xl:col-2">
                    <label for="wcode">ID</label>
                    <div class="p-inputgroup">
                        <Dropdown v-model="pre" :options="idPre" class="w-6rem"></Dropdown>
                        <InputMask type="text" id="wcode" v-model="iD" mask="99999999" class="w-full" slotChar="" />
                    </div>
                </div>

                <div class="field col-12 md:col-4 xl:col-2">
                    <label for="title">Title</label>
                    <InputText type="text" id="title" v-model="iTitle" />
                </div>

                <div class="field col-12 md:col-4 xl:col-2">
                    <label for="circle">Circle</label>
                    <AutoComplete type="text" inputId="circle"
                        v-model="iCircle" :suggestions="sCircle" optionLabel="name" modelValue="id"
                        forceSelection @complete="searchCircle" @update:modelValue="" autoOptionFocus
                        :virtualScrollerOptions="{itemSize: 34, autoSize: true}" />
                </div>

                <div class="field col-12 md:col-6 xl:col-3">
                    <label for="cv">CV</label>
                    <MultiSelect inputId="cv" v-model="iCV" showToggleAll
                        :options="sCV" display="chip" filter :selectionLimit="3"
                        optionLabel="name" optionValue="name"
                        :virtualScrollerOptions="tagsPanelOpts" @update:modelValue="">
                    </MultiSelect>
                </div>

                <div class="field col-12 md:col-6 xl:col-3">
                    <label>Age</label>
                        <span class="p-buttonset">
                            <Button v-for="item in ageOpts" :label="item.option" @click="ageButtonToggle(item.value)"
                                :text="!ageChecked(item.value)" :icon="ageIcon(item.value)" />
                        </span>
                </div>

                <template v-if="advOptions">
                    <div class="field col-12 md:col-5 xl:col-3">
                        <label for="rDate">Release Date</label>
                        <Calendar showIcon showButtonBar inputId="rDate" v-model="releaseDate" selectionMode="range"
                            :manualInput="false" dateFormat="yy-mm-dd" />
                    </div>

                    <div class="field col-12 md:col-7 xl:col-3">
                        <label for="genres">Genres</label>
                        <MultiSelect inputId="genres" v-model="iGenres" showToggleAll
                            filter :options="sGenres" display="chip" optionLabel="value" optionValue="id"
                            :virtualScrollerOptions="tagsPanelOpts" :selectionLimit="5">
                        </MultiSelect>
                    </div>

                    <div class="field col-12 md:col-4 xl:col-2">
                        <label for="series">Series</label>
                        <AutoComplete type="text" inputId="series"
                            v-model="iSeries" :suggestions="sSeries" optionLabel="name" optionValue="id"
                            forceSelection @complete="searchSeries" />
                    </div>
                    <div class="field col-12 md:col-4 xl:col-2">
                        <label for="scripter">Scripter</label>
                        <AutoComplete type="text" inputId="scripter"
                            v-model="iScripter" :suggestions="sScripter" optionLabel="name"
                            forceSelection @complete="searchScripter" />
                    </div>
                    <div class="field col-12 md:col-4 xl:col-2">
                        <label for="illustrator">Illustrator</label>
                        <AutoComplete type="text" inputId="illustrator"
                            v-model="iIllustrator" :suggestions="sIllustrator" optionLabel="name"
                            forceSelection @complete="searchIllustrator" />
                    </div>
                </template>

                <div class="field col-12 md:col-6">
                    <div class="flex md:justify-content-start">
                        <Button label="Advanced Options" @click="onAdvOpt" class="md:w-max" iconPos="right"
                            :icon="advOptions?'fa-solid fa-angles-up fa-lg':'fa-solid fa-angles-down fa-lg'" />
                    </div>
                </div>
                <div class="field col-12 md:col-6">
                    <Toast />
                    <div class="flex justify-content-between md:justify-content-end gap-3">
                        <Button label="Clear" icon="fa-regular fa-circle-xmark fa-lg" iconPos="right"
                            @click="onClear" class="w-max" />
                        <Button label="Submit" icon="fa-regular fa-circle-check fa-lg" iconPos="right"
                            @click="onSubmit" class="w-max" :loading="submitLoading" />
                    </div>
                </div>

            </div>
        </Panel>
    </div>

    <Transition name="slide-left">
        <div class="card" v-show="resultsShow">
            <Panel header="Search Results">
                <DataView :value="results" :layout="resultsLayout" paginator paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink JumpToPageDropdown" :rows="resultsPerPage">
                    <template #header>
                        <div class="flex justify-content-between">
                            <div class="flex gap-3">
                                <Dropdown v-model="sortKey" :options="sortOptions" optionLabel="label" optionValue="value"
                                    @change="sortResults(false)" placeholder="Sort by..." class="w-12rem" />
                                <Button @click="sortResults(true)" rounded :icon="sortOrderIcon" />
                            </div>
                            <div class="flex gap-3">
                                <DataViewLayoutOptions v-model="resultsLayout" class="my-auto"></DataViewLayoutOptions>
                                <Dropdown v-model="resultsPerPage" :options="resultsPerPageOpts"></Dropdown>
                            </div>
                        </div>
                    </template>
                    <template #list="slotProps">
                        <div v-for="(item, index) in slotProps.items" :key="item.id" :data-index="index">
                            <WorkListLayoutItem :item="item" :index="index" :detail_show="onDetailClick"></WorkListLayoutItem>
                        </div>
                    </template>
                    <template #grid="slotProps">
                        <div class="grid">
                            <div v-for="(item, index) in slotProps.items" :key="item.id" :data-index="index" class="col-12 xl:col-3 lg:col-4 md:col-6">
                                <WorkGridLayoutItem :item="item" :index="index" :detail_show="onDetailClick"></WorkGridLayoutItem>
                            </div>
                        </div>
                    </template>
                </DataView>
            </Panel>
        </div>
    </Transition>

    <Transition name="slide-right">
        <div class="card" v-show="detailShow">
            <Panel :header="detailID">
                <template #icons>
                    <Button label="Back" @click="toggleDetail(false)" icon="fa-solid fa-circle-chevron-left fa-lg"></Button>
                </template>
            </Panel>
        </div>
    </Transition>

</template>

<style lang="scss"></style>
