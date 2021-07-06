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
.inside {
    font-size: 10em;
    display:inline;
    width: 1.5em;
    // justify-content: space-between;
    // margin: 0 auto;
    color: #00a8cc;
    // padding: 25px, 25px, 25px, 25px;
    font-family: 'BebasNeue';
}
</style>
