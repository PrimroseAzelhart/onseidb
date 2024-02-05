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
        <div class="flex flex-column h-20rem">

        </div>
    </div>
</template>
