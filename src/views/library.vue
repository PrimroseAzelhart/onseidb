<script setup>

import { ref } from 'vue';
import axios from 'axios';

const refreshDis = ref(true);
const uhashjp = ref('');
const results = ref();

const submit = () => {
    url = '' + uhashjp.value;
    axios.get(url)
    .then(function (response) {
        console.log(response);
    })
    .catch(function (error) {
        console.log(error);
    });
};

</script>

<template>
    <div class="card">
        <div class="grid">
            <div class="col-8">
                <span class="p-float-label">
                    <InputMask class="w-full" id="uhashjp" slotChar="" mask="****************" v-model="uhashjp" />
                    <label for="uhashjp">uhashjp</label>
                </span>
            </div>
            <div class="col-2">
                <Button label="Refresh" class="w-full" icon="fa-solid fa-arrows-rotate fa-spin" :disabled="refreshDis" />
            </div>
            <div class="col-2">
                <Button label="Submit" class="w-full" :disabled="!uhashjp" @click="submit" />
            </div>
        </div>
    </div>
</template>
