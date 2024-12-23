import { ref } from 'vue';

export function useNotification() {
  const show = ref(false);
  const message = ref('');
  const type = ref<'success' | 'error'>('success');

  function showNotification(newMessage: string, newType: 'success' | 'error' = 'success', duration = 3000) {
    message.value = newMessage;
    type.value = newType;
    show.value = true;

    if (duration > 0) {
      setTimeout(() => {
        show.value = false;
      }, duration);
    }
  }

  function hideNotification() {
    show.value = false;
  }

  return {
    show,
    message,
    type,
    showNotification,
    hideNotification
  };
}