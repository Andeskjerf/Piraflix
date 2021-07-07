<template>
  <div id="container">
    <font-awesome-icon class="inside" :icon="['fas', 'film-alt']"/>
    <p class="inside">Piraflix</p>
  </div>
</template>

<script lang="ts">
import { Vue } from 'vue-class-component'

export default class Logo extends Vue {

}
</script>

<style scoped lang="scss">
#container {
  // min-width: 60em;
  // overflow: visible;
  width: 100%;
  height: 100%;
  background-color: aqua;
}

.inside {
    font-size: 10em;
    display:inline;
    width: 1.5em;
    // justify-content: space-between;
    // margin: 0 auto;
    color: $color-logo;
    // padding: 25px, 25px, 25px, 25px;
    font-family: 'Bebas Neue';
}
</style>
