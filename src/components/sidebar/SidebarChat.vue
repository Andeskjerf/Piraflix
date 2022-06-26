<template>
  <div id="sidebarChat">
    <transition-group name="chatList">
      <user-tile
        v-for="message in chatMessages"
        :key="message.id"
        :tile-data="message"
      />
    </transition-group>
  </div>
  <input
    v-model="chatInput"
    class="inputField"
    placeholder="Type a message..."
    type="text"
    @keyup.enter="chatInputEntered"
  />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import UserTile from "@/components/UserTile.vue";
import { UserTileInterface } from "@/data/UserTileInterface";

interface ChatData {
  chatMessages: UserTileInterface[];
  chatInput: "";
}

export default defineComponent({
  components: {
    UserTile,
  },
  props: {
    roomId: {
      type: String,
      default: "",
    },
  },
  sockets: {
    join(val: string): void {
      this.addMessage(val);
    },
    leave(val: string): void {
      this.addMessage(val);
    },
    messageSend(val: string): void {
      this.addMessage(val);
    },
  },
  data(): ChatData {
    return {
      chatMessages: [],
      chatInput: "",
    };
  },
  methods: {
    chatInputEntered: function (): void {
      if (this.chatInput !== "") {
        this.$socket.client.emit("messageSend", {
          message: this.chatInput,
          roomId: this.roomId,
        });
        this.chatInput = "";
      }
    },
    addMessage(val: string): void {
      const message = JSON.parse(val);
      const obj: UserTileInterface = {
        id: message.id,
        message: message.message,
        identifier: message.user.identifier,
        username: message.user.username,
        statusMessage: message.isStatus,
      };
      this.chatMessages.unshift(obj);
    },
  },
});
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
