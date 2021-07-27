<template>
  <div id="roomCreateWrapper" class="boxShadow roundBorder">
    <input-label labelIcon="magnet" label="Magnet link"></input-label>
    <input v-model="checked" type="text" class="inputField focusBorder roundBorder">
  </div>
</template>

<script>
import InputLabel from './InputLabel.vue'
export default {
  name: 'Room creation',
  props: {
    magnetLink: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      checked: this.magnetLink
    }
  },
  components: { InputLabel },
  watch: {
    magnetLink: function (newVal, oldVal) {
      if (newVal !== oldVal) this.checked = newVal
    },
    checked: function (newVal, oldVal) {
      if (newVal !== oldVal) {
        this.$emit('magnet-link', newVal)
      }
    }
  }
}
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
