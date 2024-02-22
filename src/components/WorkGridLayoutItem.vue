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

const getCoverUrl = (id) => {
    const category = id.substring(0, 2);
    var categoryPath = '';
    switch (category) {
        case 'RJ':
            categoryPath = 'doujin';
            break;
        case 'BJ':
            categoryPath = 'books';
            break;
        case 'VJ':
            categoryPath = 'professional';
            break;
    }
    const idStr = id.substring(2);
    const idLen = idStr.length;
    const idNumber = parseInt(idStr);
    const coverPathNumber = (parseInt(idNumber / 1000) + 1) * 1000;
    const coverPathStr = `${category}${String(coverPathNumber).padStart(idLen, '0')}`;
    console.log(coverPathStr);
    const coverUrl = `https://img.dlsite.jp/modpub/images2/work/${categoryPath}/${coverPathStr}/${id}_img_main.webp`
    return coverUrl;
};

</script>

<template>
    <div class="card">
        <div class="flex flex-column gap-2">
            <Image :src="getCoverUrl(item.id)" :alt="item.id" imageClass="flex w-full" preview />
            <div :title="item.title" class="text-xl font-bold text-900 grid-title">
                {{ item.title }}
            </div>
            <div class="flex gap-2 h-2rem flex-wrap">
                <div class="white-space-nowrap text-lg my-auto text-overflow-ellipsis">{{ item.circle + ' /' }}</div>
                <div v-for="(cv, idx) in item.cv" class="my-auto">
                    <Chip v-if="idx<1" :label="cv" class="h-full white-space-nowrap"></Chip>
                    <div v-if="idx==1">other</div>
                </div>
            </div>
            <div class="flex justify-content-between inline">
                <div class="my-auto white-space-nowrap">{{ isoTimeToString(item.release_date) }}</div>
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
