<template>
  <transition name="fade" mode="out-in">
    <video-player v-show="showTorrent" id="videoPlayerContainer"></video-player>
  </transition>
  <div class="landing">
      <logo id="logo"></logo>
      <div class="center">
        <room-creation-box v-bind:magnet="inputText" v-on:magnet-link="checkMagnetLink"></room-creation-box>
        <big-button
          btnText="Host room"
          :buttonActive=roomValid
          @clicked="createRoom"></big-button>
      </div>
    </div>
</template>

<script>
import Logo from '@/components/Logo.vue'
import BigButton from '@/components/BigButton.vue'
import RoomCreationBox from '@/components/RoomCreationBox.vue'
import WebTorrent from 'webtorrent'
import VideoPlayer from '@/components/VideoPlayer.vue'
import axios from 'axios'

const client = new WebTorrent()
const path = 'http://127.0.0.1:5000/api/rooms'

export default {
  components: {
    Logo,
    RoomCreationBox,
    BigButton,
    VideoPlayer
  },
  methods: {
    createRoom: function () {
      const payload = {
        magnet: this.magnet
      }

      axios.post(path, payload)
        .then((res) => {
          console.log(res.data.room.id)
          this.joinRoom(res.data.room)
        })
        .catch((error) => {
          console.log(error)
        })
    },
    checkMagnetLink: function (value) {
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
    getRoom: function (roomId) {
      axios.get(path + '?roomId=' + roomId)
        .then((res) => {
          console.log(res.data.room)
          if (res.data.room !== undefined) {
            console.log(res.data.room.id)
            this.joinRoom(res.data.room)
          } else {
            console.log('No room found with this ID')
            history.pushState(null, '', '/')
          }
        })
        .catch((error) => {
          console.log(error)
        })
    },
    joinRoom: function (room) {
      var data = JSON.parse(room)
      console.log('Joining room ' + data.id)
      history.pushState(null, '', data.id)
      client.add(data.magnet, function (torrent) {
        const file = torrent.files.find(function (file) {
          return file.name.endsWith('.mp4')
        })
        console.log(file)
        // this.showTorrent = true
        // this.torrentFile = file
        // this.torrentFile.appendTo('#videoPlayer')
        file.renderTo('video#videoPlayer')
      })
      this.roomValid = false
      this.showTorrent = true
    }

  },
  data () {
    return {
      inputText: '',
      magnet: 'magnet:?xt=urn:btih:08ada5a7a6183aae1e09d831df6748d566095a10&dn=Sintel&tr=udp%3A%2F%2Fexplodie.org%3A6969&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.empire-js.us%3A1337&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=wss%3A%2F%2Ftracker.btorrent.xyz&tr=wss%3A%2F%2Ftracker.fastcast.nz&tr=wss%3A%2F%2Ftracker.openwebtorrent.com&ws=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2F&xs=https%3A%2F%2Fwebtorrent.io%2Ftorrents%2Fsintel.torrent',
      roomValid: true,
      showTorrent: false
    }
  },
  mounted () {
    var path = this.$route.path.substr(1)
    if (path.length > 0) {
      this.getRoom(path)
    }
  }
}
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
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active,
.slide-leave-active {
  transition: all 0.8s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-enter-from,
.slide-leave-to {
  transform: translateY(5em);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(5em);
  opacity: 0;
}

#logo {
  padding-top: 10em;
  padding-bottom: 2.5em;
  text-align: center;
}
</style>
