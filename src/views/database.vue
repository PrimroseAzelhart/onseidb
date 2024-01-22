<script setup>

import { ref, onMounted, computed } from 'vue'
import { databaseService } from '@/service/api.js'

const dbKey = ['circle', 'cv', 'tag']

const db = new databaseService();
const localLastUpdate = ref();
const message = ref([]);
const dbLastUpdate = ref([]);
const needUpdate = ref([]);
const updateButtonDisabled = ref(true);

const msg = {
    'none': {'severity': 'info', 'text': 'No local database found'},
    'outdated': {'severity': 'warn', 'text': 'Local database is outdated, update available'},
    'error': {'severity': 'error', 'text': 'Unable to check for updates from server'},
    'updated': {'severity': 'success', 'text': 'Local database is updated'}
};

onMounted(() => {
    localLastUpdate.value = localStorage.getItem('update');
    if (localLastUpdate.value) {
        db.checkUpdate()
        .then((data) => {
            dbLastUpdate.value = data;
            for (var key of dbKey) {
                if (dbLastUpdate.value[key] > localLastUpdate.value) {
                    needUpdate.value.push(key);
                }
            }
            if (needUpdate.value.length === 0) {
                addMessage('updated');
                return;
            }
            updateButtonDisabled.value = false;
        })
        .catch((error) => {
            addMessage('error');
        });
    } else {
        needUpdate.value = dbKey;
        addMessage('none');
        updateButtonDisabled.value = false;
    }
});

const getLocalLastUpdate = computed(() => {
    return localLastUpdate.value ? (new Date(localLastUpdate.value * 1000).toString()) : '';
});

const addMessage = (type) => {
    message.value = [{ severity: msg[type]['severity'], content: msg[type]['text']}];
};

const updateDB = () => {
    for (var key of needUpdate.value) {
        db.get(key);
    }
    needUpdate.value = [];
    localLastUpdate.value = Date.now() / 1000;
    localStorage.setItem('update', localLastUpdate.value.toString());
    addMessage('updated');
};

</script>

<template>
    <div class="card">
        <h5>Local database</h5>
        <p>Last update: {{ getLocalLastUpdate }}</p>
        <transition-group name="p-message" tag="div">
            <Message v-for="msg of message" :severity="msg.severity" :key="msg.content" :closable="false">{{ msg.content }}</Message>
        </transition-group>
        <Button label="Update" :disabled="updateButtonDisabled" @click="updateDB"></Button>
    </div>
</template>
