<template>
  <div id="sidebarChat">
    <transition-group name="chatList">
      <div class="chatMessage roundBorder" v-for="message in chatMessages" :key="message.id">
        <Avatar id="chatAvatar" :name=message.username />
        <div id="chatMsgContent">
          <p id="username">{{ message.username }}</p>
          <p id="message" :class="{ statusMessage: message.statusMessage }">{{ message.message }}</p>
        </div>
      </div>
    </transition-group>
  </div>
  <input v-model="chatInput" v-on:keyup.enter="chatInputEntered" class="inputField" placeholder="Type a message..." type="text" />
</template>

<script lang="ts">
import Avatar from 'vue-boring-avatars'
import { defineComponent } from 'vue'

interface MessageData {
  id: string,
  message: string,
  username: string,
  statusMessage: boolean
}

interface ChatData {
  chatMessages: MessageData[]
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
    addMessage (val: any): void {
      const message = JSON.parse(val)
      const obj: MessageData = {
        id: message.id,
        message: message.message,
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
    Avatar
  }
})
</script>

<style lang="scss" scoped>
#sidebarChat {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  bottom: 0;
  right: 0;
  left: 0;
}
#sidebarChat {
  display: flex;
  flex-direction: column-reverse;
  flex: 1 1 auto;
  overflow-y: auto;
  height: 100%;
  position: relative;
}
.chatMessage {
  display: inline-flex;
  margin: 0.5em 1em 0.5em 1em;
  p {
    color: $color-text;
    margin: 0.25em 1em 0.25em 1em;
  }
}
#username {
  font-weight: bold;
}

#chatAvatar {
  margin-top: 0.5em;
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

#chatMsgContent {
  max-width: 235px;
}

#message {
  word-break: break-all;
}

</style>
