<template>
  <div id="statusField">
    <!-- <font-awesome-icon class=icon :icon=labelIcon></font-awesome-icon> -->
    <p class="label">{{ label }}</p>
  </div>
</template>

<script>
export default {
  name: "TorrentStatus",
  props: {
    magnetLink: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      label: "Waiting for file",
    };
  },
};
</script>

<style>
#statusField {
  display: flex;
  align-items: center;
  /* background-color: brown; */
  max-height: 50px;
}
</style>
