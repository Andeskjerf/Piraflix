<template>
  <div id="inputLabel">
    <font-awesome-icon class="icon" :icon="labelIcon"></font-awesome-icon>
    <p class="label textColor">{{ label }}</p>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "InputLabel",
  props: {
    labelIcon: {
      type: String,
      default: "",
    },
    label: {
      type: String,
      default: "",
    },
  },
});
</script>

<style>
#inputLabel {
  display: flex;
  align-items: center;
  max-height: 50px;
}
</style>
