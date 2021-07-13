<template>
  <div>
    <video id="videoPlayer"></video>
    <div id="videoSidebarContainer">
      <sidebar-content />
    </div>
  </div>
</template>

<script>
import SidebarContent from './SidebarContent.vue'
export default {
  components: { SidebarContent }

}
</script>

<style lang="scss" scoped>
#videoPlayer {
  min-width: 100%;
  min-height: 100%;

  width: 100%;
  height: 100%;

  position: relative;
  display: table-cell;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
}
#videoSidebarContainer {
  display: table-cell;
  width: 20em;
  height: 100%;
  background-color: $color-primary-dark;
  vertical-align: bottom;
}

</style>
