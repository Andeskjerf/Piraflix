<template>
  <div id="sidebarHeader">
    <p class="label logoText">Piraflix</p>
    <div id="infoContainer">
      <p id="roomMemberCount" class="infoText">{{ memberCount }} online</p>
      <font-awesome-icon
        class="iconButton scaleHover halfOpacity opaqueHover"
        :icon="['fas', 'users']"
        @click="toggleUserList"
      />
      <font-awesome-icon
        class="iconButton scaleHover halfOpacity opaqueHover"
        :icon="['fas', 'cog']"
        @click="toggleSettingsModal"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  props: {
    memberCount: { type: Number, default: -1 },
  },
  emits: ["toggleUserList", "toggleSettingsModal"],
  methods: {
    toggleUserList() {
      this.$emit("toggleUserList");
    },
    toggleSettingsModal() {
      this.$emit("toggleSettingsModal");
    },
  },
});
</script>

<style lang="scss" scoped>
#sidebarHeader {
  display: flex;
  border-bottom: 1px solid $color-primary-light;
  position: relative;
  top: 0;
  width: 100%;
  p {
    margin: 0.5em;
  }
}

#infoContainer {
  position: absolute;
  display: flex;
  align-content: center;
  align-items: center;
  right: 10px;

  &p {
    padding: 0;
    margin: 0;
  }
  align-self: center;
}
</style>
