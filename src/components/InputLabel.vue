<template>
  <div id="inputLabel">
    <font-awesome-icon class=icon :icon=labelIcon></font-awesome-icon>
    <p class="label">{{ label }}</p>
  </div>
</template>

<script>
export default {
  name: 'Input label',
  props: ['labelIcon', 'label']
}
</script>

<style>
#inputLabel {
  display: flex;
  align-items: center;
  /* background-color: brown; */
  max-height: 50px;
}
</style>
