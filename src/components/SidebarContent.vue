<template>
  <div>
    <div id="sidebarContent">
      <div id="sidebarHeader">
        <p class="label logoText">Piraflix</p>
        <div id="infoContainer">
          <p class="infoText" id="roomMemberCount">{{ memberCount }} online</p>
          <font-awesome-icon id="userIconButton" :icon="['fas', 'users']"/>
        </div>
      </div>
      <sidebar-chat :roomId="roomId" />
    </div>
  </div>
</template>

<script lang="ts">
import SidebarChat from './SidebarChat.vue'
import { defineComponent } from 'vue'

export default defineComponent({
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
})
</script>

<style lang="scss" scoped>
#sidebarContent {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}
#sidebarHeader {
  display: flex;
  border-bottom: 1px solid $color-primary-light;
  position: relative;
  top: 0;
  width: 100%;
  p {
    margin: 0.5em;
  }
}

#infoContainer {
  position: absolute;
  display: flex;
  align-content: center;
  align-items: center;
  right: 10px;

  &p {
    padding: 0;
    margin: 0;
    // margin: 0 5em 0 0;
  }
  align-self: center;
}

#userIconButton {
  color: $color-text;
  opacity: 0.5;

  // position: absolute;

  padding-left: 0.5em;
  padding-right: 0.5em;

  width: 32px;
  height: 32px;

  transition: all 100ms ease-out;

  &:hover {
    opacity: 1.0;
    transform: scale(1.05);
  }
}

</style>
