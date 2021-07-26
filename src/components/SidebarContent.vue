<template>
  <div id="sidebarContent">
    <div id="sidebarHeader">
      <p class="label logoText">Piraflix</p>
    </div>
    <sidebar-chat :roomId="roomId" />
  </div>
</template>

<script>
import SidebarChat from './SidebarChat.vue'

export default {
  props: { roomId: String },
  components: { SidebarChat }
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

</style>
