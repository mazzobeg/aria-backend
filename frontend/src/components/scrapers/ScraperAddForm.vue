<template>
  <div class="row border border-success rounded my-3">
    <form @submit.prevent="addScraper">
      <h3 class="my-3">Ajouter un scraper</h3>
      <div class="my-3">
        <label class="form-label" for="name">Name</label>
        <input class="form-control" type="text" name="name" id="name" v-model="form.name" />
      </div>
      <div class="my-3">
        <label class="form-label" for="name">Content</label>
        <textarea class="form-control" type="text" name="content" id="content" v-model="form.content"></textarea>
      </div>
      <div class="my-3">
        <label class="form-label" for="name">Kwargs</label>
        <input class="form-control" type="text" name="content" id="content" v-model="form.kwargs" />
      </div>
      <button type="submit" class="btn btn-success mb-3">Ajouter</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import ScrapersService from '@/services/ScrapersService';
import { ref } from 'vue';

const form = ref({
  name: '',
  content: '',
  kwargs: ''
});

const addScraper = () => {
  ScrapersService.addScraperByProperties(form.value.name, form.value.content, form.value.kwargs);
  form.value.name = '';
  form.value.content = '';
  form.value.kwargs = '';
};

</script>