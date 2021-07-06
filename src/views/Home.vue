<template>
  <div class="landing">
    <logo id="logo"></logo>
    <BigButton id="createRoom" class="centerVertically" btnText="Create room"></BigButton>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'
import BigButton from '@/components/BigButton.vue'
import Logo from '@/components/Logo.vue'

@Options({
  components: {
    BigButton,
    Logo
  }
})
export default class Home extends Vue {}
</script>
<style scoped lang="scss">
.landing {
  height: 100%;
  // position: relative;
}

#logo {
    margin: 10em;
    text-align: center;
}
#createRoom {
    // margin: 5%;
    // text-align: center;
}

.centerVertically {
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
