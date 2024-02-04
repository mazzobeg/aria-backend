<template>
    <div class="card row my-3">
        <div class="card-header">
            <div class="row">
                <div class="col">
                    <h5 class="card-title">{{ props.scraper.name }}</h5>
                </div>
                <div class="col text-end">
                    <button class="btn btn-secondary me-1" @click="manageLock">{{ updateModeManager.textToDisplay }}</button>
                    <button class="btn btn-warning me-1" @click="updateScraper"
                        :disabled="!updateModeManager.changesDone">Update</button>
                    <button class="btn btn-danger me-1" @click="deleteScraper">Delete</button>
                    <button class="btn btn-primary" @click="runScraper" :disabled="isLoading">{{ isLoading ? 'Loading...' :
                        'Run' }}</button>
                </div>
            </div>
        </div>
        <div class="card-body">
            <p v-if="!updateModeManager.isUpdateMode" class="card-text">{{ scraper.content }}</p>
            <textarea v-if="updateModeManager.isUpdateMode" class="form-control" type="text" name="scraper-content"
                id="scraper-content" v-model="scraper.content" @input="enableUpdate"></textarea>
        </div>
        <div class="card-footer text-body-secondary">
            <span v-if="!updateModeManager.isUpdateMode">{{ scraper.kwargs }}</span>
            <input v-if="updateModeManager.isUpdateMode" class="form-control" type="input" name="scraper-kwargs"
                id="scraper-kwargs" v-model="scraper.kwargs" @input="enableUpdate">
        </div>
    </div>
</template>

<script setup lang="ts">
import { PropType, defineProps, ref, toRaw, watch } from 'vue';
import Scraper from '@/models/Scraper';
import ScrapersService from '@/services/ScrapersService';

const props = defineProps({
    scraper: {
        type: Object as PropType<Scraper>,
        required: true
    }
});

const scraper = ref(props.scraper);

const deleteScraper = () => ScrapersService.deleteScraper(props.scraper);
const updateScraper = () => {
    updateModeManager.value.changesDone = false;
    ScrapersService.updateScraper(scraper.value);
}

const updateModeManager = ref({
    textToDisplay: 'Unlock',
    isUpdateMode: false,
    changesDone: false,
});

const enableUpdate = () => updateModeManager.value.changesDone = true;

const manageLock = () => {
    updateModeManager.value.isUpdateMode = !updateModeManager.value.isUpdateMode;
    updateModeManager.value.textToDisplay = updateModeManager.value.isUpdateMode ? 'Lock' : 'Unlock';
};

const isLoading = ref(false);

const runScraper = async () => {
    isLoading.value = true;
    await ScrapersService.runScraper(props.scraper);
    isLoading.value = false;
};

</script>