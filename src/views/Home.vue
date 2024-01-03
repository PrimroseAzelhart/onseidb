<script setup>

import axios from 'axios'

axios.defaults.headers["Content-Type"] = "application/x-www-form-urlencoded";

const onClick = () => {
    axios.post('http://api.onsei.fans/search', {
            option: 'code'
        })
        .then(function (response) {
            console.log(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
}
</script>

<template>
    <Button label="DB" @click="onClick"></Button>
</template>
