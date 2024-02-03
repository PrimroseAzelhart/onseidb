<script setup>

import { ref, onMounted, computed } from 'vue';
import { useToast } from 'primevue/usetoast';
import axios from 'axios'
import { databaseService } from '@/service/api.js'

import AutoComplete from 'primevue/autocomplete';
import Calendar from 'primevue/calendar';
import DataView from 'primevue/dataview';
import Fieldset from 'primevue/fieldset';

const pre = ref('RJ');
const iD = ref(null);
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

const inputGroup = [iD, iTitle, iCircle, iCV, iAge, releaseDate, releaseAfter, releaseBefore, iGenres, iSeries, iScripter, iIllustrator]
const keyGroup = ['id', 'title', 'circle', 'cv', 'age', 'rel_date', 'rel_after', 'rel_before', 'genre', 'series', 'scripter', 'illustrator']
const selectionGroup = [aCircle, sCV, sGenres, aSeries, aScripter, aIllustrator]
const selectionKey = ['circle', 'cv', 'genre', 'series', 'scripter', 'illustrator']

const results = ref([]);
const advOptions = ref(false);
const resultsPerPage = ref(10);

const submitLoading = ref(false);

const sortKey = ref('date');
const sortAscend = ref(false);

const resultsShow = ref(true);
const detailShow = ref(false);

const db = new databaseService();

const toast = useToast();

const axiosInstance = axios.create()
axiosInstance.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded';

onMounted(() => {
    for (var i = 0; i < selectionKey.length; i++) {
        const res = db.retrieve(selectionKey[i]);
        if (res) {
            selectionGroup[i].value = JSON.parse(res);
        }
    }
});

const codeLabel = [
    {label: 'RJ', command: () => {pre.value = 'RJ'}},
    {label: 'BJ', command: () => {pre.value = 'BJ'}},
    {label: 'VJ', command: () => {pre.value = 'VJ'}}
];

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
            postProcess()

            submitLoading.value = false;
            console.log(results.value);
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

const onReleaseDateInput = (value) => {
    releasePeriodDisable.value = value === null ? false : true;
};

const onReleasePeriodInput = (value) => {
    releaseDateDisable.value = value === null ? false : true;
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

const getSeverity = (value) => {
    switch (value) {
        case 0:
            return 'success';
        case 1:
            return 'warning';
        case 2:
            return 'danger';
    }
};

const isDiscount = (item) => {
    return item.price !== item.price_current;
};

const isoTimeToString = (time) => {
    const date = new Date(time);
    const dateStr = `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`;
    return dateStr;
};

const getTrophyStyle = (item) => {
    switch (item) {
        case 'day':
            return 'bronze';
        case 'week':
            return 'silver';
        case 'month':
            return 'gold';
        case 'year':
            return 'diamond';
    }
};

const toggleResults = (show) => {
    if (show) {
        detailShow.value = false;
        setTimeout(() => {
            resultsShow.value = true;
        }, 500)
    } else {
        resultsShow.value = false;
        setTimeout(() => {
            detailShow.value = true;
        }, 500)
    }
};

const debug = (value) => {
    console.log(value);
};

</script>

<template>

    <div class="card">
        <Panel header="Search Options" toggleable>
            <div class="grid p-fluid">

                <div class="field col-12 md:col-4">
                    <label for="wcode">ID</label>
                    <div class="p-inputgroup">
                        <SplitButton :label="pre" :model="codeLabel" />
                        <InputMask type="text" id="wcode" v-model="iD" mask="99999999"
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
                        v-model="iCircle" :suggestions="sCircle" optionLabel="name" modelValue="id"
                        dropdown forceSelection @complete="searchCircle" @update:modelValue="debug" />
                </div>

                <div class="field col-12 md:col-6">
                    <label for="cv">CV</label>
                    <MultiSelect inputId="cv" placeholder="Select CV" v-model="iCV" showToggleAll
                        :options="sCV" display="chip" filter :selectionLimit="3"
                        optionLabel="name" optionValue="name"
                        :virtualScrollerOptions="tagsPanelOpts" @update:modelValue="">
                    </MultiSelect>
                </div>
                <div class="field col-12 md:col-6">
                    <label>Age</label>
                        <span class="p-buttonset">
                            <Button v-for="item in ageOpts" :label="item.option" @click="ageButtonToggle(item.value)"
                                :text="!ageChecked(item.value)" :icon="ageIcon(item.value)" />
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
                        <label for="genres">Genres</label>
                        <MultiSelect inputId="genres" placeholder="Select genre" v-model="iGenres" showToggleAll
                            filter :options="sGenres" display="chip" optionLabel="value" optionValue="id"
                            :virtualScrollerOptions="tagsPanelOpts" :selectionLimit="5">
                        </MultiSelect>
                    </div>

                    <div class="field col-12 md:col-4">
                        <label for="series">Series</label>
                        <AutoComplete type="text" inputId="series" placeholder="Select series"
                            v-model="iSeries" :suggestions="sSeries" optionLabel="name" optionValue="id"
                            dropdown forceSelection @complete="searchSeries" />
                    </div>
                    <div class="field col-12 md:col-4">
                        <label for="scripter">Scripter</label>
                        <AutoComplete type="text" inputId="scripter" placeholder="Select scripter"
                            v-model="iScripter" :suggestions="sScripter" optionLabel="name"
                            dropdown forceSelection @complete="searchScripter" />
                    </div>
                    <div class="field col-12 md:col-4">
                        <label for="illustrator">Illustrator</label>
                        <AutoComplete type="text" inputId="illustrator" placeholder="Select illustrator"
                            v-model="iIllustrator" :suggestions="sIllustrator" optionLabel="name"
                            dropdown forceSelection @complete="searchIllustrator" />
                    </div>
                </template>

                <div class="field col-12 md:col-6">
                    <div class="flex md:justify-content-start">
                        <Button label="Advanced Options" @click="onAdvOpt" class="md:w-max" iconPos="right"
                            :icon="advOptions?'fa-solid fa-angles-up fa-lg':'fa-solid fa-angles-down fa-lg'" />
                        <!-- <Button label="show" @click="toggleResults(detailShow)"></Button> -->
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

    <Transition name="slide-results">
        <div class="card" v-show="resultsShow">
            <Panel header="Search Results">
                <DataView :value="results" paginator paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink JumpToPageDropdown" :rows="resultsPerPage">
                    <template #header>
                        <div class="flex justify-content-between">
                            <div class="flex gap-3">
                                <Dropdown v-model="sortKey" :options="sortOptions" optionLabel="label" optionValue="value"
                                    @change="sortResults(false)" placeholder="Sort by..." class="w-12rem" />
                                <Button @click="sortResults(true)" rounded :icon="sortOrderIcon" />
                            </div>
                            <Dropdown v-model="resultsPerPage" :options="resultsPerPageOpts" class=""></Dropdown>
                        </div>
                    </template>
                    <template #list="slotProps">
                        <div v-for="(item, index) in slotProps.items" :key="item.id" :data-index="index" class="col-12">
                            <Fieldset :legend="item.id">
                                <div class="flex flex-row align-items-center justify-content-between p-2 gap-3 w-full h-13rem">
                                    <div class="flex flex-column h-full w-12rem justify-content-between">
                                        <Image src="onseidb-logo.svg" preview alt="Cover" class="flex h-9rem w-full"/>
                                        <Tag :value="item.age" :severity="getSeverity(item.age)" class="absolute mt-2 ml-2 opacity-50 text-lg"></Tag>
                                        <div class="flex flex-row w-full justify-content-evenly">
                                            <div class="border-round-3xl border-2 border-primary px-2 py-1 text-xs flex flex-row gap-2 align-items-center">
                                                <i class="fa-solid fa-star text-yellow-400"></i>
                                                <p v-if="item.rate" class="inline"> {{ item.rate }} </p>
                                                <p v-else class="inline">N/A</p>
                                            </div>
                                            <div class="border-round-3xl border-2 border-primary px-2 py-1 text-xs flex flex-row gap-2 align-items-center">
                                                <i class="fa-solid fa-circle-down fa-lg"></i>
                                                <p v-if="item.rate" class="inline"> {{ item.dl }} </p>
                                                <p v-else class="inline">N/A</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex flex-column justify-content-between h-full flex-grow-1 w-1rem">
                                        <div :title="item.title" class="text-2xl font-bold text-900 text-overflow-ellipsis overflow-hidden white-space-nowrap">
                                            {{ item.title }}
                                        </div>
                                        <div class="flex gap-3 h-2rem">
                                            <div class="my-auto">{{ isoTimeToString(item.release_date) }}</div>
                                            <Chip v-if="item.last_update" :label="isoTimeToString(item.last_update)" class="h-full bg-primary">
                                                <template #icon>
                                                    <i class="fa-solid fa-wrench">&nbsp;</i>
                                                </template>
                                            </Chip>
                                        </div>
                                        <div class="flex gap-2 h-2rem">
                                            <div class="white-space-nowrap text-lg my-auto">{{ item.circle + ' /' }}</div>
                                            <div v-for="(cv, idx) in item.cv">
                                                <Chip v-if="idx<5" :label="cv" class="h-full"></Chip>
                                                <Chip v-if="idx==5" label="..." class="h-full"></Chip>
                                            </div>
                                        </div>
                                        <div class="h-2rem">
                                            <div v-if="item.genre" class="flex gap-2">
                                                <div v-for="genre in item.genre" >
                                                    <Tag :value="genre" class="text-sm" rounded />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="flex flex-column justify-content-between align-items-end h-full min-w-max">
                                        <div v-if="item.rank_first" class="flex flex-column gap-1">
                                            <div class="flex gap-2 h-2rem justify-content-end">
                                                <div v-for="i in item.rank_first.voice">
                                                    <i class="fa-solid fa-medal fa-fw" :class="getTrophyStyle(i)"></i>
                                                </div>
                                            </div>
                                            <div class="flex gap-2 h-2rem justify-content-end">
                                                <div v-for="i in item.rank_first.all">
                                                    <i class="fa-solid fa-trophy fa-fw" :class="getTrophyStyle(i)"></i>
                                                </div>
                                            </div>
                                        </div>
                                        <div v-else></div>
                                        <div class="flex align-items-end flex-column">
                                            <div v-if="isDiscount(item)" class="text-sm line-through">￥{{ item.price }}</div>
                                            <div class="text-2xl font-semibold">￥{{ item.price_current }}</div>
                                        </div>
                                    </div>
                                </div>
                            </Fieldset>
                        </div>
                    </template>
                </DataView>
            </Panel>
        </div>
    </Transition>

    <Transition name="slide-detail">
        <div class="card" v-show="detailShow">

        </div>
    </Transition>

</template>

<style lang="scss">

.p-tieredmenu {
    width: auto;
    min-width: auto;
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

.p-dataview-header {
    margin-bottom: 1rem;
    border-width: 0;
}

.p-dataview-emptymessage {
    display: none;
}

.p-panel {
    border: 0;
}

.p-fieldset-legend-text {
    font-size: large;
}

.slide-detail-enter-active,
.slide-results-enter-active {
    transition: all 0.5s ease;
    transition-delay: 0.6s;
}

.slide-detail-leave-active,
.slide-results-leave-active {
    transition: all 0.3s ease;
}

.slide-results-enter-from,
.slide-results-leave-to {
    transform: translateX(-20px);
    opacity: 0;
}

.slide-detail-enter-from,
.slide-detail-leave-to {
    transform: translateX(20px);
    opacity: 0;
}


.bronze {
    background: linear-gradient(30deg, brown, coral);
    // -webkit-background-clip: text;
    background-clip:text;
    color: transparent;
    font-size: 1.5rem;
}

.silver {
    background: linear-gradient(30deg, silver, snow);
    // -webkit-background-clip: text;
    background-clip:text;
    color: transparent;
    font-size: 1.5rem;
}

.gold {
    background: linear-gradient(30deg, gold, khaki);
    // -webkit-background-clip: text;
    background-clip:text;
    color: transparent;
    font-size: 1.5rem;
}

.diamond {
    background: linear-gradient(30deg, cyan, white);
    // -webkit-background-clip: text;
    background-clip:text;
    color: transparent;
    font-size: 1.5rem;
}

</style>
