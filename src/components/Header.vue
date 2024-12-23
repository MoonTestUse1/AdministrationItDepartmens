<template>
  <header class="bg-slate-800 text-white py-3">
    <div class="container mx-auto px-4">
      <div class="flex flex-col sm:flex-row justify-between items-center gap-2">
        <div class="flex items-center space-x-3">
          <Building2Icon :size="28" class="text-blue-400" />
          <div class="text-center sm:text-left">
            <h1 class="text-lg sm:text-xl font-semibold">Администрация КАО</h1>
            <p class="text-xs sm:text-sm text-slate-300">Портал технической поддержки</p>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <PhoneIcon :size="18" class="text-blue-400" />
          <div class="text-center sm:text-left">
            <p class="text-xs text-slate-300">Поддержка:</p>
            <p class="text-sm font-semibold">8 (800) 123-45-67</p>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Building2Icon, PhoneIcon } from 'lucide-vue-next';
</script>