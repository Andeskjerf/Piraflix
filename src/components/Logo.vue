<template>
  <div id="container">
    <font-awesome-icon class="inside logoText" :icon="['fas', 'film-alt']" />
    <p class="inside logoText">Piraflix</p>
  </div>
</template>

<script lang="ts">
import { Vue } from "vue-class-component";

export default class Logo extends Vue {}
</script>

<style scoped lang="scss">
#container {
  width: 100%;
  height: 100%;
  background-color: aqua;
}

.inside {
  font-size: 10em;
  display: inline;
  width: 1.5em;
}
</style>
