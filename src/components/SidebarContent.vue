<template>
  <div>
    <div id="sidebarContent">
      <div id="sidebarHeader">
        <p class="label logoText">Piraflix</p>
        <div id="infoContainer">
          <p class="infoText" id="roomMemberCount">{{ memberCount }} online</p>
          <font-awesome-icon id="userIconButton" :icon="['fas', 'users']" v-on:click="toggleUserList"/>
        </div>
      </div>
      <sidebar-chat :roomId="roomId" />
      <transition name="slide-in">
        <div v-show="userListExpanded" id="userListContainer" class="boxShadow" v-on:click="toggleUserList">
          <div id="userListWrapper">
            <user-tile :tileData="user" v-for="user in users" :key="user" />
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script lang="ts">
import SidebarChat from './SidebarChat.vue'
import { defineComponent } from 'vue'
import UserTile from './UserTile.vue'
import { UserTileModel } from '@/interfaces/UserTileModel'

export default defineComponent({
  props: { roomId: String },
  components: { SidebarChat, UserTile },
  sockets: {
    roomUserCount (data) {
      const parsed = JSON.parse(data)

      this.users = []
      for (var item of parsed) {
        const obj: UserTileModel = {
          identifier: item.identifier,
          username: item.username,
          onlyUsername: true
        }

        this.users.push(obj)
      }

      this.memberCount = this.users.length
    }
  },
  methods: {
    toggleUserList () {
      this.userListExpanded = !this.userListExpanded
    }
  },
  mounted () {
    this.users = []
  },
  data () {
    return {
      memberCount: 0,
      userListExpanded: false,
      users: {} as UserTileModel[]
    }
  }
})
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

#userIconButton {
  color: $color-text;
  opacity: 0.5;

  padding-left: 0.5em;
  padding-right: 0.5em;

  width: 32px;
  height: 32px;

  transition: all 100ms ease-out;

  &:hover {
    opacity: 1.0;
    transform: scale(1.05);
  }
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

#userListWrapper {
  display: flex;
  flex-direction: column;
  flex: 1 1 auto;
  overflow-y: auto;
  height: 100%;
  position: relative;
  margin: 1em;
}

.slide-in-enter-active {
  transition: all 0.3s ease-in-out;
}

.slide-in-leave-active {
  transition: all 0.4s ease-in-out;;
}

.slide-in-enter-from,
.slide-in-leave-to {
  transform: translate(300px, -50%) !important;
  opacity: 0;
}

</style>
