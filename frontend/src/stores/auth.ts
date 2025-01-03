import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '@/types/auth';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const isAdmin = ref(false);

  const isAuthenticated = computed(() => !!user.value);

  function setUser(newUser: User | null) {
    user.value = newUser;
  }

  function setAdmin(value: boolean) {
    isAdmin.value = value;
  }

  async function login(lastName: string, password: string): Promise<boolean> {
    try {
      const formData = new FormData();
      formData.append('username', lastName);
      formData.append('password', password);

      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        return false;
      }

      const userData = await response.json();
      setUser(userData);
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  }

  async function adminLogin(username: string, password: string): Promise<boolean> {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch('/api/auth/admin/login', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        return false;
      }

      setAdmin(true);
      return true;
    } catch (error) {
      console.error('Admin login error:', error);
      return false;
    }
  }

  function logout() {
    user.value = null;
    isAdmin.value = false;
  }

  return {
    user,
    isAdmin,
    isAuthenticated,
    setUser,
    setAdmin,
    login,
    adminLogin,
    logout
  };
});