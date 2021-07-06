<template>
  <button type="button">
    {{ btnText }}
  </button>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component'

@Options({
  props: {
    btnText: String
  }
})
export default class BigButton extends Vue {
  btnText!: string;
}
</script>

<style scoped lang="scss">
button {
  padding: 0.75cm 1.5cm;
  text-align: center;
  text-decoration: none;
  color: aliceblue;
  font-size: 32px;
  background-color: #00a8cc;
  border: none;
  border-radius: 12px;
}
p {
  color: #fff;
}
</style>
