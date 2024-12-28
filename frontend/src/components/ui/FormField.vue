<template>
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
      {{ label }}<span v-if="required" class="text-red-500">*</span>
    </label>
    
    <div class="relative">
      <div v-if="icon" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <component :is="icon" size="18" class="text-gray-400" />
      </div>

      <template v-if="type === 'select'">
        <select
          :value="modelValue"
          @input="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
          :required="required"
          class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Выберите {{ label.toLowerCase() }}</option>
          <option v-for="option in options" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </template>

      <template v-else>
        <input
          :type="type"
          :value="modelValue"
          @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
          :required="required"
          class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
      </template>
    </div>

    <slot name="help"></slot>
  </div>
</template>

<script setup lang="ts">
import { Component } from 'vue';

defineProps<{
  modelValue: string;
  label: string;
  type?: string;
  required?: boolean;
  disabled?: boolean;
  placeholder?: string;
  help?: string;
  icon?: Component;
  size?: number | string; // Добавляем поддержку как числа, так и строки
  options?: Array<{ value: string; label: string }>;
}>();

defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();
</script>