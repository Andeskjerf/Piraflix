<template>
  <button @click="handleClick()" :class="!buttonActive ? 'disabled' : ''">
    {{ btnText }}
  </button>
</template>

<script lang="ts">
import { SetupContext, defineComponent } from 'vue'

export default defineComponent({
  name: 'Button',
  props: ['btnText', 'buttonActive'],
  emits: ['clicked'],
  setup (props, context: SetupContext): any {
    const handleClick = () => {
      if (props.buttonActive) { context.emit('clicked') }
    }

    return { handleClick }
  }
})
</script>

<style scoped lang="scss">
button {
  // padding: 0.75cm 1.5cm;
  text-align: center;
  text-decoration: none;
  color: aliceblue;
  font-size: 38px;
  width: 7em;
  height: 2em;
  border: none;
  border-radius: $border-radius;
  transition-duration: 300ms;
  box-shadow: $box-shadow;

  background-color: $color-button;
  &:hover {
    background-color: $color-on-hover;
  }
}

.disabled {
  background-color: $color-button-disabled;
  &:hover {
    background-color: $color-button-disabled;
  }
}

p {
  color: $color-text;
}
</style>
