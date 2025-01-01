import axios from 'axios'
import type { AxiosInstance } from 'axios'
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance
  }
} 