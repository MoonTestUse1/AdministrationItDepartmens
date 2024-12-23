<template>
  <footer class="bg-slate-800 text-white">
    <div class="container mx-auto px-4 py-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <h3 class="text-sm font-semibold mb-2 flex items-center gap-2">
            <PhoneIcon :size="16" class="text-blue-400" />
            Контактная информация
          </h3>
          <div class="space-y-1 text-sm text-slate-300">
            <p>8 (800) 123-45-67</p>
            <p>support@admincity.ru</p>
          </div>
        </div>
        <div>
          <h3 class="text-sm font-semibold mb-2 flex items-center gap-2">
            <ClockIcon :size="16" class="text-blue-400" />
            Режим работы
          </h3>
          <div class="space-y-1 text-sm text-slate-300">
            <p>Пн-Пт: 9:45 - 17:45</p>
            <p>Сб-Вс: выходной</p>
          </div>
        </div>
        <div>
          <h3 class="text-sm font-semibold mb-2 flex items-center gap-2">
            <MailIcon :size="16" class="text-blue-400" />
            Техподдержка
          </h3>
          <div class="space-y-1 text-sm text-slate-300">
            <p>Время реакции: до 2 часов</p>
            <p>support@admincity.ru</p>
          </div>
        </div>
      </div>
      <div class="border-t border-slate-700 mt-3 pt-2 text-center text-xs text-slate-400">
        <p>© 2024 Администрация КАО. Все права защищены.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { PhoneIcon, ClockIcon, MailIcon } from 'lucide-vue-next';
</script>