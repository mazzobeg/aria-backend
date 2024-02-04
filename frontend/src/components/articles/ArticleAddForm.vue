<template>
  <div class="row border border-success rounded my-3">
    <form @submit.prevent="addArticle">
      <h3 class="my-3">Ajouter un article</h3>
      <div class="my-3">
        <label class="form-label" for="name">Title</label>
        <input class="form-control" type="text" name="title" id="title" v-model="form.title" />
      </div>
      <div class="my-3">
        <label class="form-label" for="name">Content</label>
        <textarea class="form-control" type="text" name="content" id="content" v-model="form.content"></textarea>
      </div>
      <div class="my-3">
        <label class="form-label" for="name">link</label>
        <input class="form-control" type="text" name="content" id="content" v-model="form.link" />
      </div>
      <button type="submit" class="btn btn-success mb-3">Ajouter</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import ArticlesService from '@/services/ArticlesService';
import { ref } from 'vue';

const form = ref({
  title: '',
  content: '',
  link: ''
});

const addArticle = () => {
  ArticlesService.addArticleByProperties(form.value.title, form.value.content, form.value.link);
  form.value.title = '';
  form.value.content = '';
  form.value.link = '';
};

</script>