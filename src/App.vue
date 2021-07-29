<template>
  <body>
    <router-view />
  </body>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  beforeUnmount () {
    // this.$socket.client.disconnect()
  }
})
</script>

<style lang="scss">
html {
    background-color: $color-background;
    width: 100%;
    height: 100%;

    body {
      margin: 0;
    }
}

* {
    font-family: $font;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
</style>
