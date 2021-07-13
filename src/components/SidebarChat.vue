<template>
  <div id="sidebarChat">
    <div id="sidebarChatMessages">
      <transition-group name="chatList">
        <div class="chatMessage" v-for="message in chatMessages.reverse()" :key="message.id">
          <p>{{ message.message }}</p>
        </div>
      </transition-group>
    </div>
    <input v-model="chatInput" v-on:keyup.enter="chatInputEntered" class="inputField" placeholder="Type a message..." type="text" />
  </div>
</template>

<script>
export default {
  methods: {
    chatInputEntered: function (val) {
      console.log(this.chatInput)
      if (this.chatInput !== '') {
        this.chatMessages.push({
          id: this.chatMessagesIndex,
          message: this.chatInput
        })
        this.chatMessagesIndex++
        this.chatInput = ''
      }
    }
  },
  data () {
    return {
      chatMessages: [],
      chatMessagesIndex: 0,
      chatInput: ''
    }
  }
}
</script>

<style lang="scss" scoped>
#sidebarChat {
  display: flex;
  flex-direction: column;
  height: 100%;
  // overflow: hidden;
}
#sidebarChatMessages {
  display: flex;
  flex-direction: column-reverse;
  flex: 1 1 auto;
  overflow-y: auto;
  height: 0px;
}
.chatMessage {
  p {
    color: $color-text;
    margin: 0.5em 1em;
  }
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
