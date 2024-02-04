<template>
  <div class="row">
    <div class="col">
      <h2>Liste des Articles</h2>
    </div>
  </div>
  <div class="row">
    <div class="col">
      <span class="btn btn-primary me-2" @click="fetchArticles">Refresh</span>
      <div class="btn-group">
        <a :class="`btn btn-primary ${articleDisplayMode == ArticleDisplayMode.ALL ? 'active' : ''}`"
          @click="articleDisplayMode = ArticleDisplayMode.ALL">Tous</a>
        <a :class="`btn btn-primary ${articleDisplayMode == ArticleDisplayMode.UNREAD ? 'active' : ''}`"
          @click="articleDisplayMode = ArticleDisplayMode.UNREAD">Non lu</a>
        <a :class="`btn btn-primary ${articleDisplayMode == ArticleDisplayMode.READ ? 'active' : ''}`"
          @click="articleDisplayMode = ArticleDisplayMode.READ">Lu</a>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-xl-6 pe-xl-4">
      <ArticleAddForm />
    </div>
    <div class="col-xl-6 ps-xl-4">
      <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ComputedRef, computed, onMounted, ref } from 'vue';
import ArticlesService from '@/services/ArticlesService';
import { Article } from '@/models/Article';
import ArticleAddForm from './ArticleAddForm.vue';
import ArticleCard from './ArticleCard.vue';

const articles: ComputedRef<Article[]> = computed(() =>
  ArticlesService.listArticle.filter((article) => {
    switch (articleDisplayMode.value) {
      case ArticleDisplayMode.READ:
        return article.state === 'READ';
      case ArticleDisplayMode.UNREAD:
        return article.state === 'UNREAD';
      default:
        return true;
    }
  })
);

const fetchArticles = async () => {
  await ArticlesService.getArticles();
};

onMounted(fetchArticles);

enum ArticleDisplayMode {
  ALL,
  READ,
  UNREAD
}

const articleDisplayMode = ref(ArticleDisplayMode.ALL);

</script>