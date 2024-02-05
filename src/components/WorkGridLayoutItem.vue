<script setup>

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
    <div class="card">
        <div class="flex flex-column gap-2">
            <img :src="'onseidb-logo.svg'" preview alt="Cover" class="flex h-9rem"/>
            <div :title="item.title" class="text-xl font-bold text-900 grid-title">
                {{ item.title }}
            </div>
            <div class="flex gap-2 h-2rem">
                <div class="white-space-nowrap text-lg my-auto">{{ item.circle + ' /' }}</div>
                <div v-for="(cv, idx) in item.cv" class="my-auto">
                    <Chip v-if="idx<1" :label="cv" class="h-full"></Chip>
                    <div v-if="idx==1">and other</div>
                </div>
            </div>
            <div class="flex justify-content-between inline">
                <div class="my-auto">{{ isoTimeToString(item.release_date) }}</div>
                <div class="text-2xl font-semibold">￥{{ item.price_current }}</div>
            </div>
            <Button label="Detail" @click="detail_show(item.id)"></Button>
        </div>
    </div>
</template>

<style lang="scss">
.grid-title {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
}
</style>
