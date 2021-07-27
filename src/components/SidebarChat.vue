<template>
  <div id="sidebarChat">
    <transition-group name="chatList">
      <user-tile :tileData="message" v-for="message in chatMessages" :key="message.id"/>
    </transition-group>
  </div>
  <input v-model="chatInput" v-on:keyup.enter="chatInputEntered" class="inputField" placeholder="Type a message..." type="text" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import UserTile from './UserTile.vue'
import { UserTileModel } from '@/interfaces/UserTileModel'

interface ChatData {
  chatMessages: UserTileModel[]
  chatInput: ''
}

export default defineComponent({
  props: { roomId: String },
  sockets: {
    join (val): void {
      this.addMessage(val)
    },
    leave (val): void {
      this.addMessage(val)
    },
    messageSend (val): void {
      this.addMessage(val)
    }
  },
  methods: {
    chatInputEntered: function (): void {
      if (this.chatInput !== '') {
        this.$socket.client.emit('messageSend', { message: this.chatInput, roomId: this.roomId })
        this.chatInput = ''
      }
    },
    addMessage (val: string): void {
      console.log(val)
      const message = JSON.parse(val)
      const obj: UserTileModel = {
        id: message.id,
        message: message.message,
        identifier: message.user.identifier,
        username: message.user.username,
        statusMessage: message.isStatus
      }
      this.chatMessages.unshift(obj)
    }
  },
  data (): ChatData {
    return {
      chatMessages: [],
      chatInput: ''
    }
  },
  components: {
    UserTile
  }
})
</script>

<style lang="scss" scoped>
#sidebarChat {
  display: flex;
  flex-direction: column-reverse;
  flex: 1 1 auto;
  overflow-y: auto;
  height: 100%;
  position: relative;
}

.chatList-enter-active,
.chatList-leave-active {
  transition: all 1s ease;
}
.chatList-enter-from,
.chatList-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

</style>
