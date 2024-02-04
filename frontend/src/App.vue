<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">ARIA</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <router-link class="nav-link" to="/scrapers">Scrapers</router-link>
          <router-link class="nav-link" to="/articles">Articles</router-link>
        </div>
      </div>
    </div>
  </nav>
  <div class="container py-4">
    <router-view></router-view>
  </div>
</template>

<script lang="ts" setup>
</script>
