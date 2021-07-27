<template>
  <transition name="slide-fade" mode="out-in" @after-leave="renderVideo">
    <video-player v-if="showTorrent" id="videoPlayerContainer" :room="room" v-bind:watch-video="showTorrent" @closeVideo="leaveRoom"></video-player>
    <div v-else class="landing">
      <logo id="logo"></logo>
      <div class="center">
        <room-creation-box v-bind:magnet="inputText" v-on:magnet-link="checkMagnetLink"></room-creation-box>
        <big-button
          btnText="Host room"
          :buttonActive=roomValid
          @clicked="createRoom"></big-button>
      </div>
      <div id="footer">
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import Logo from '@/components/Logo.vue'
import BigButton from '@/components/BigButton.vue'
import RoomCreationBox from '@/components/RoomCreationBox.vue'
import WebTorrent, { Torrent } from 'webtorrent'
import VideoPlayer from '@/components/VideoPlayer.vue'
import { createRoom, getRoom } from '@/api/RoomAPI'
import { Room } from '@/api/models/RoomModel'
import { defineComponent } from 'vue'

const client = new WebTorrent()

export default defineComponent({
  components: {
    Logo,
    RoomCreationBox,
    BigButton,
    VideoPlayer
  },
  methods: {
    createRoom: async function (): Promise<void> {
      var room = await createRoom(this.magnet)
      if (room.id !== '-1') {
        this.joinRoom(room)
      } else {
        console.log('Invalid room ID')
      }
    },
    checkMagnetLink: function (value: string): void {
      console.log(this.roomValid)
      var isMagnetLink = value.includes('magnet:?xt=urn:btih:')
      if (isMagnetLink && !this.roomValid) {
        this.roomValid = true
        this.magnet = value
      } else if (!isMagnetLink && this.roomValid) {
        this.roomValid = false
        this.magnet = value
      }
    },

    joinRoom: function (room: Room): void {
      console.log('Joining room ' + room.id)
      history.pushState(null, '', room.id)
      this.room = room

      this.roomValid = false
      this.showTorrent = true
    },
    leaveRoom: function (): void {
      history.pushState(null, '', '/')
      this.magnet = ''
      this.room = new Room()
      this.roomValid = false
      this.showTorrent = false
      this.torrent.destroy()
      this.$socket.client.emit('leave')
    },
    renderVideo (): void {
      if (this.room.id !== '-1') {
        try {
          client.add(this.room.magnet, (torrent: Torrent) => {
            this.torrent = torrent
            const file = torrent.files.find(function (file) {
              return file.name.endsWith('.mp4')
            })
            if (file !== undefined) {
              file.renderTo('video#videoPlayer')
            } else {
              console.log('Error while getting file data from torrent!')
              this.leaveRoom()
            }
          })
          this.$socket.client.emit('join', { roomId: this.room.id })
        } catch (error) {
          console.log('Error while initating torrent / video player!')
          console.log(error)
        }
      }
    }
  },
  data () {
    return {
      inputText: '',
      roomValid: false,
      showTorrent: false,
      magnet: '',
      room: new Room(),
      torrent: {

      } as Torrent
    }
  },
  async mounted () {
    var path = this.$route.path.substr(1)
    if (path.length > 0) {
      var room = await getRoom(path)
      if (room.id !== '-1') {
        this.joinRoom(room)
      } else {
        console.log('No room found with this ID')
        history.pushState(null, '', '/')
      }
    }
  },
  beforeUnmount () {
    if (this.room !== null) {
      this.$socket.client.emit('leave', { roomId: this.room.id })
    }
  }
})
</script>
<style scoped lang="scss">
#videoPlayerContainer {
  position: absolute;
  display: table;
  top: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #000;
}

.landing {
  min-width: 45em;
}

.slide-fade-enter-active,
.slide-enter-active {
  transition: all 0.5s ease-out;
}

.slide-fade-leave-active,
.slide-leave-active {
  transition: all 0.5s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
}

#logo {
  padding-top: 10em;
  padding-bottom: 0em;
  text-align: center;
}
</style>
