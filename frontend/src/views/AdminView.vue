import AdminChatList from '@/components/admin/AdminChatList.vue'
import AdminChatView from '@/components/admin/AdminChatView.vue'
import ChatNotification from '@/components/ChatNotification.vue'

const chats = ref([])
const selectedChat = ref(null)
const showChatNotification = ref(false)
const chatNotificationMessage = ref('')

const loadChats = async () => {
  try {
    const response = await fetch('/api/chat/admin/chats/', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    if (response.ok) {
      chats.value = await response.json()
    }
  } catch (error) {
    console.error('Error loading chats:', error)
  }
}

const handleChatSelect = (chat) => {
  selectedChat.value = chat
}

onMounted(() => {
  loadChats()
  const interval = setInterval(loadChats, 30000)
  
  onUnmounted(() => {
    clearInterval(interval)
  })
})

<div class="grid grid-cols-1 md:grid-cols-12 gap-6 mb-6">
  <!-- Чаты -->
  <div class="md:col-span-4">
    <AdminChatList
      :chats="chats"
      :selected-chat-id="selectedChat?.id"
      @select-chat="handleChatSelect"
    />
  </div>
  
  <!-- Область чата -->
  <div class="md:col-span-8">
    <AdminChatView
      :chat="selectedChat"
      :current-user-id="currentUser.id"
    />
  </div>
</div>

<!-- Уведомления -->
<ChatNotification
  :show="showChatNotification"
  :message="chatNotificationMessage"
  @close="showChatNotification = false"
  @action="handleChatNotificationAction"
/> 