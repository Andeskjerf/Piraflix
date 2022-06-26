<template>
  <button :class="!active ? 'disabled' : ''" @click="handleClick()">
    {{ text }}
  </button>
</template>

<script lang="ts">
import { SetupContext, defineComponent } from "vue";

export default defineComponent({
  name: "CustomButton",
  props: {
    text: {
      type: String,
      default: "btnText",
    },
    active: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["clicked"],
  setup(props, context: SetupContext) {
    const handleClick = () => {
      if (props.active) {
        context.emit("clicked");
      }
    };

    return { handleClick };
  },
});
</script>

<style scoped lang="scss">
button {
  // padding: 0.75cm 1.5cm;
  text-align: center;
  text-decoration: none;
  color: $color-text;
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
