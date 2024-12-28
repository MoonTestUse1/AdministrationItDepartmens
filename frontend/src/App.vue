<template>
  <div class="min-h-screen flex flex-col bg-slate-100">
    <Header />
    <main class="flex-grow container mx-auto px-3 sm:px-4 py-4 sm:py-8">
      <router-view></router-view>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
</script>