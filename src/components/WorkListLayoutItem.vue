<script setup>

import Fieldset from 'primevue/fieldset';

const props = defineProps({
    item: {
        type: Object,
        default: () => ({})
    },
    index: {
        type: Number,
        default: 0
    },
    detail_show: {
        type: Function,
        default: () => {}
    }
});

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

const isDiscount = (item) => {
    return item.price !== item.price_current;
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

</script>

<template>
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
                    <Button label="Detail" class="" @click="detail_show(true)"></Button>
                </div>
            </div>
        </div>
    </Fieldset>

</template>
