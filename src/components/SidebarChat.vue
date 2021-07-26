<template>
  <div id="sidebarChat">
    <div id="sidebarChatMessages">
      <transition-group name="chatList">
        <div class="chatMessage roundBorder" v-for="message in chatMessages" :key="message.id">
          <Avatar id="chatAvatar" name=message.username />
          <div>
            <p id="username">{{ message.username }}</p>
            <p id="message" :class="{ statusMessage: message.statusMessage }">{{ message.message }}</p>
          </div>
        </div>
      </transition-group>
    </div>
    <input v-model="chatInput" v-on:keyup.enter="chatInputEntered" class="inputField" placeholder="Type a message..." type="text" />
  </div>
</template>

<script>
import Avatar from 'vue-boring-avatars'
export default {
  props: { roomId: String },
  sockets: {
    join (val) {
      this.addMessage(val)
    },
    leave (val) {
      this.addMessage(val)
    },
    messageSend (val) {
      this.addMessage(val)
    }
  },
  methods: {
    chatInputEntered: function (val) {
      if (this.chatInput !== '') {
        this.$socket.client.emit('messageSend', { message: this.chatInput, roomId: this.roomId })
        this.chatInput = ''
      }
    },
    addMessage (val) {
      const message = JSON.parse(val)
      const obj = {
        id: message.id,
        message: message.message,
        username: message.user.username,
        statusMessage: message.isStatus
      }
      this.chatMessages.unshift(obj)
    }
  },
  data () {
    return {
      chatMessages: [],
      chatInput: ''
    }
  },
  components: {
    Avatar
  }
}
</script>

<style lang="scss" scoped>
#sidebarChat {
  display: flex;
  flex-direction: column;
  height: 100%;
}
#sidebarChatMessages {
  display: flex;
  flex-direction: column-reverse;
  flex: 1 1 auto;
  overflow-y: auto;
  height: 0px;
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
  align-self: center;
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
