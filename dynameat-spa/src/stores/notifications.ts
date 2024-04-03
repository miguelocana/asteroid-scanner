import { defineStore } from 'pinia'

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    show: false,
    message: '',
    detail: '',
    type: 'success',
  }),
  actions: {
    setNotification({ message = '', detail = '', type = 'success' }) {
      this.show = true
      this.message = message
      this.detail = detail
      this.type = type

      setTimeout(() => {
        this.show = false
      }, 10000)
    }
  }
})
