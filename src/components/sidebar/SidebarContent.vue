<template>
  <div>
    <div id="sidebarContent">
      <sidebar-header
        :member-count="memberCount"
        @toggle-user-list="toggleUserList"
        @toggle-settings-modal="toggleSettingsModal"
      />
      <sidebar-chat :room-id="roomId" />
      <transition name="slide-in">
        <div
          v-show="userListExpanded"
          id="userListContainer"
          class="boxShadow"
          @click="toggleUserList"
        >
          <div class="columnFlexScroll">
            <user-tile v-for="_user in users" :key="_user" :tile-data="_user" />
          </div>
        </div>
      </transition>
      <transition name="slide-in">
        <div
          v-show="settingsModalOpen"
          id="userListContainer"
          class="boxShadow"
          @click.self="toggleSettingsModal"
        >
          <div id="optionsWrapper" class="columnFlexScroll">
            <h1 id="optionsLabel" class="label textBold textColor">Options</h1>
            <div>
              <div id="usernameWrapper">
                <p class="textBold textColor">Username</p>
                <big-button
                  text="Apply"
                  :active="usernameInputChanged"
                  @clicked="changeUsername"
                />
              </div>
              <input
                id="usernameInput"
                v-model="currentUsername"
                class="inputField roundBorder"
                @keyup.enter="changeUsername"
              />
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts">
import SidebarChat from "@/components/sidebar/SidebarChat.vue";
import SidebarHeader from "@/components/sidebar/SidebarHeader.vue";
import { defineComponent, inject } from "vue";
import UserTile from "@/components/UserTile.vue";
import { UserTileInterface } from "@/data/UserTileInterface";
import { UserModel } from "@/api/models/UserModel";
import BigButton from "@/components/CustomButton.vue";

export default defineComponent({
  components: { SidebarChat, SidebarHeader, UserTile, BigButton },
  props: {
    roomId: {
      type: String,
      default: "",
    },
  },
  setup() {
    const user: UserModel | undefined = inject("userData");
    return { user };
  },
  sockets: {
    roomUserCount(data) {
      const parsed = JSON.parse(data);

      this.users = [];
      for (const item of parsed) {
        const obj: UserTileInterface = {
          identifier: item.identifier,
          username: item.username,
          onlyUsername: true,
        };

        this.users.push(obj);
      }

      this.memberCount = this.users.length;
    },
  },
  data() {
    return {
      memberCount: 0,
      userListExpanded: false,
      settingsModalOpen: false,
      users: {} as UserTileInterface[],
      currentUsername: "",
      usernameInputChanged: false,
      buttonStyle: {
        fontSize: "16px",
        width: "1em",
        height: "0.5em",
      },
    };
  },
  watch: {
    currentUsername() {
      if (
        this.user !== undefined &&
        this.currentUsername.trim() &&
        this.user.username !== this.currentUsername
      ) {
        this.usernameInputChanged = true;
      } else this.usernameInputChanged = false;
    },
  },
  mounted() {
    this.users = [];
    if (this.user !== undefined) {
      this.currentUsername = this.user.username;
    } else this.currentUsername = "UNDEFINED";
  },
  methods: {
    toggleUserList() {
      if (this.settingsModalOpen) this.settingsModalOpen = false;
      this.userListExpanded = !this.userListExpanded;
    },
    toggleSettingsModal() {
      if (this.userListExpanded) this.userListExpanded = false;
      this.settingsModalOpen = !this.settingsModalOpen;
    },
    changeUsername() {
      if (this.user !== undefined && this.usernameInputChanged) {
        this.user.username = this.currentUsername;
        this.$socket.client.emit("usernameChange", this.user.username);
        this.usernameInputChanged = false;
        this.settingsModalOpen = false;
      }
    },
  },
});
</script>

<style lang="scss" scoped>
#sidebarContent {
  display: flex;
  flex-direction: column;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

#userListContainer {
  height: 85%;
  width: 300px;
  position: absolute;
  right: 0;
  top: 50%;
  bottom: 50%;
  transform: translateY(-50%);

  border-radius: $border-radius 0 0 $border-radius;

  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 1;
}

.slide-in-enter-active {
  transition: all 0.3s ease-in-out;
}

.slide-in-leave-active {
  transition: all 0.4s ease-in-out;
}

.slide-in-enter-from,
.slide-in-leave-to {
  transform: translate(300px, -50%) !important;
  opacity: 0;
}

#optionsLabel {
  font-size: 24px;
  margin: 0.5em 0.5em 0 0.5em;
}

#optionsWrapper {
  overflow-x: clip;
  pointer-events: none;

  > div {
    margin-left: 1em;
    margin-right: 1em;
    margin-top: 0;
    margin-bottom: 0;

    pointer-events: auto;
  }
}

#usernameInput {
  height: 0px;
}

#usernameWrapper {
  display: flex;
  justify-content: space-between;

  button {
    height: 32px;
    width: 68px;

    align-self: center;
  }
}
</style>
