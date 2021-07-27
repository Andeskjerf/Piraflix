<template>
  <div id="inputLabel">
    <font-awesome-icon class=icon :icon=labelIcon></font-awesome-icon>
    <p class="label">{{ label }}</p>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Input label',
  props: ['labelIcon', 'label']
})
</script>

<style>
#inputLabel {
  display: flex;
  align-items: center;
  max-height: 50px;
}
</style>
