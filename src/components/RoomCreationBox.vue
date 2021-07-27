<template>
  <div id="roomCreateWrapper" class="boxShadow roundBorder">
    <input-label labelIcon="magnet" label="Magnet link"></input-label>
    <input v-model="checked" type="text" class="inputField focusBorder roundBorder">
  </div>
</template>

<script lang="ts">
import InputLabel from './InputLabel.vue'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Room creation',
  props: {
    magnetLink: {
      type: String,
      default: ''
    }
  },
  data (): any {
    return {
      checked: this.magnetLink
    }
  },
  components: { InputLabel },
  watch: {
    magnetLink: function (newVal: string, oldVal: string): void {
      if (newVal !== oldVal) this.checked = newVal
    },
    checked: function (newVal: string, oldVal: string): void {
      if (newVal !== oldVal) {
        this.$emit('magnet-link', newVal)
      }
    }
  }
})
</script>

<style lang="scss" scoped>
#roomCreateWrapper {
  width: 50%;
  min-width: 35em;
  max-width: 60em;
  background-color: $color-primary;

  padding: 2em;
  margin: 3em 2em;

  input {
    margin-top: 0.5em;
  }
}
</style>
