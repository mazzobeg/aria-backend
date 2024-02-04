<template>
    <div :class="`card row my-3 ${summaryEmpty ? '' : 'border border-primary'}`">
        <div class="card-header" id="article-header">
            <div class="row">
                <div class="col" id="article-title" @click="displayContent = !displayContent">
                    <h5 v-if="!updateModeManager.isUpdateMode" class="card-title">{{ props.article.title }}</h5>
                    <input v-if="updateModeManager.isUpdateMode" class="form-control" type="text" name="title" id="title"
                        v-model="article.title" @input="enableUpdate" />
                </div>
                <div class="col text-end">
                    <button class="btn btn-secondary me-1" @click="manageLock">{{ updateModeManager.textToDisplay
                    }}</button>
                    <button class="btn btn-warning me-1" @click="updateScraper"
                        :disabled="!updateModeManager.changesDone">Update</button>
                    <button class="btn btn-danger me-1" @click="deleteScraper">Delete</button>
                    <button class="btn btn-primary" @click="summarizeArticle" :disabled="isLoading">{{ isLoading ?
                        'Loading...' :
                        'Summarize' }}</button>
                    <button class="btn btn-warning" @click="ArticlesService.switchState(article)">{{ props.article.state
                    }}</button>
                    <button class="btn btn-primary" @click="translateArticle" :disabled="isTranslationLoading">{{
                        isTranslationLoading ?
                        'Loading...' :
                        'Translate' }}</button>
                </div>
            </div>
        </div>
        <div class="card-header">
            <ul class="nav nav-tabs card-header-tabs">
                <li class="nav-item">
                    <a :class="`nav-link ${contentDisplay == DisplayMode.CONTENT ? 'active' : ''}`"
                        @click="contentDisplay = DisplayMode.CONTENT">Content</a>
                </li>
                <li class="nav-item">
                    <a :class="`nav-link ${contentDisplay == DisplayMode.SUMMARY ? 'active' : ''}`"
                        @click="contentDisplay = DisplayMode.SUMMARY">Summary</a>
                </li>
                <li class="nav-item">
                    <a :class="`nav-link ${contentDisplay == DisplayMode.SUMMARY_TRANSLATION ? 'active' : ''}`"
                        @click="contentDisplay = DisplayMode.SUMMARY_TRANSLATION">Summary </a>
                </li>
            </ul>
        </div>
        <div class="card-body" v-if="displayContent">
            <div v-if="contentDisplay == DisplayMode.CONTENT">
                <p v-if="!updateModeManager.isUpdateMode" class="card-text">{{ props.article.content }}</p>
                <textarea v-if="updateModeManager.isUpdateMode" class="form-control" type="text" name="article-content"
                    id="article-content" v-model="article.content" @input="enableUpdate"></textarea>
            </div>
            <div v-if="contentDisplay == DisplayMode.SUMMARY">
                <p v-if="!updateModeManager.isUpdateMode" class="card-text">{{ props.article.summary }}</p>
                <textarea v-if="updateModeManager.isUpdateMode" class="form-control" type="text" name="article-summary"
                    id="article-summary" v-model="article.summary" @input="enableUpdate"></textarea>
            </div>
            <div v-if="contentDisplay == DisplayMode.SUMMARY_TRANSLATION">
                <p v-if="!updateModeManager.isUpdateMode" class="card-text">{{ props.article.summaryTranslation }}</p>
                <textarea v-if="updateModeManager.isUpdateMode" class="form-control" type="text"
                    name="article-summary-translation" id="article-summary-translation" v-model="article.summaryTranslation"
                    @input="enableUpdate"></textarea>
            </div>
        </div>
        <div class="card-footer text-body-secondary">
            <a :href="article.link">{{ props.article.link }}</a>
        </div>
    </div>
</template>

<script setup lang="ts">
import { PropType, defineProps, ref, toRaw, watch } from 'vue';
import { Article } from '@/models/Article';
import ArticlesService from '@/services/ArticlesService';

const props = defineProps({
    article: {
        type: Object as PropType<Article>,
        required: true
    }
});

const summaryEmpty = ref(props.article.summary == null || props.article.summary == '');

const article = ref(props.article);

const deleteScraper = () => ArticlesService.deleteArticle(props.article);
const updateScraper = () => {
    updateModeManager.value.changesDone = false;
    ArticlesService.updateArticle(article.value);
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

const summarizeArticle = async () => {
    isLoading.value = true;
    await ArticlesService.summarizeArticle(props.article);
    isLoading.value = false;
};

const displayContent = ref(false);

enum DisplayMode {
    CONTENT,
    SUMMARY,
    SUMMARY_TRANSLATION
}

const contentDisplay = ref(DisplayMode.CONTENT);

const isTranslationLoading = ref(false);

const translateArticle = async () => {
    isTranslationLoading.value = true;
    await ArticlesService.translateArticle(props.article);
    isTranslationLoading.value = false;
};

</script>

<style>
#article-header:hover {
    background-color: white;
}

#article-title:hover {
    cursor: pointer;
}

a:hover {
    cursor: pointer;
}
</style>