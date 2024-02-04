<template>
  <div class="row">
    <h2>Liste des scrapers</h2>
    <span class="btn btn-primary" @click="fetchScrapers">Refresh</span>
  </div>
  <div class="row">
    <div class="col-xl-6 pe-xl-4">
      <ScraperAddForm />
    </div>
    <div class="col-xl-6 ps-xl-4">
      <ScraperCard v-for="scraper in scrapers" :key="scraper.name" :scraper="scraper" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ComputedRef, computed, onMounted } from 'vue';
import ScrapersService from '@/services/ScrapersService';
import Scraper from '@/models/Scraper';
import ScraperAddForm from './ScraperAddForm.vue';
import ScraperCard from './ScraperCard.vue';

const scrapers: ComputedRef<Scraper[]> = computed(() => ScrapersService.listScraper);

const fetchScrapers = async () => {
  await ScrapersService.getScrapers();
};

onMounted(fetchScrapers);

</script>