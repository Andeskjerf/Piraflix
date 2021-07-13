<template>
  <div id="roomCreateWrapper">
    <input-label labelIcon="magnet" label="Magnet link"></input-label>
    <input v-model="checked" type="text" class="inputField focusBorder roundBorder">
    <!-- <torrent-status-field></torrent-status-field> -->
  </div>
</template>

<script>
import InputLabel from './InputLabel.vue'
// import TorrentStatusField from './TorrentStatusField.vue'
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
  background-color: $color-primary-dark;
  box-shadow: $box-shadow;
  border-radius: $border-radius;

  padding: 2em;
  margin: 2em;

  input {
    margin-top: 0.5em;
  }
}
</style>
