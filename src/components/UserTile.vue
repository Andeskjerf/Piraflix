<template>
  <div class="chatMessage roundBorder">
    <Avatar id="chatAvatar" :name=tileData.username />
    <div id="chatMsgContent" class="textColor">
      <p class="textBold" :class="{ verticalCenter: tileData.message === undefined }">{{ tileData.username }}</p>
      <p v-if="tileData.message !== undefined" id="message" :class="{ statusMessage: tileData.statusMessage }">{{ tileData.message }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Avatar from 'vue-boring-avatars'
import { UserTileInterface } from '@/data/UserTileInterface'

export default defineComponent({
  props: {
    tileData: {
      type: Object as () => UserTileInterface,
      required: true
    }
  },
  components: {
    Avatar
  }
})
</script>

<style lang="scss" scoped>
#chatMsgContent {
  max-width: 235px;
  display: table-cell;
  position: relative;
}

#message {
  word-break: break-word;
}

.chatMessage {
  display: inline-flex;
  margin: 0.5em 0.75em 0.5em 0.75em;
  p {
    margin: 0.25em 1em 0.25em 1em;
  }
}

#chatAvatar {
  margin-top: 0.5em;
}
</style>
