<template>
  <div id="sidebarContent">
    <div id="sidebarHeader">
      <p class="label logoText">Piraflix</p>
      <div id="infoContainer">
        <p class="infoText" id="roomMemberCount">Watching: {{ memberCount }}</p>
        <!-- <p class="infoText" id="roomMemberCount"></p> -->
      </div>
    </div>
    <sidebar-chat :roomId="roomId" />
  </div>
</template>

<script>
import SidebarChat from './SidebarChat.vue'

export default {
  props: { roomId: String },
  components: { SidebarChat },
  sockets: {
    roomUserCount (data) {
      this.memberCount = data
    }
  },
  data () {
    return {
      memberCount: 0
    }
  }
}
</script>

<style lang="scss" scoped>
#sidebarContent {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
#sidebarHeader {
  display: flex;
  border-bottom: 1px solid $color-primary-light;
  p {
    margin: 0.5em;
  }
}

#infoContainer {
  position: absolute;
  right: 10px;

  p {
    padding: 0;
    margin: 0;
  }
  align-self: center;
}

</style>
