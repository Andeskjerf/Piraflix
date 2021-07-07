<template>
  <transition name="fade" mode="out-in">
    <div v-show="showTorrent" id="videoPlayerContainer">
      <video id="videoPlayer"></video>
      <div id="videoSidebar"></div>
    </div>
  </transition>
  <div  class="landing">
      <!-- <vue-element-loading /> -->
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

const client = new WebTorrent()

export default {
  components: {
    Logo,
    RoomCreationBox,
    BigButton
    // Slider1
  },
  methods: {
    createRoom: function () {
      client.add(this.magnet, function (torrent) {
        const file = torrent.files.find(function (file) {
          return file.name.endsWith('.mp4')
        })
        console.log(file)
        // this.showTorrent = true
        // this.torrentFile = file
        // this.torrentFile.appendTo('#videoPlayer')
        file.renderTo('video#videoPlayer')
      })
      this.showTorrent = true
    },
    checkMagnetLink: function (value) {
      console.log(this.roomValid)
      var isMagnetLink = value.includes('magnet:?xt=urn:btih:')
      if (isMagnetLink && !this.roomValid) {
        console.log('wow!')
        this.roomValid = true
        this.magnet = value
      } else if (!isMagnetLink && this.roomValid) {
        this.roomValid = false
        this.magnet = value
      }
    }

  },
  watch: {
    // torrentFile: function () {
    //   this.showTorrent = true
    //   this.torrentFile.appendTo('body')
    // }
  },
  data () {
    return {
      inputText: '',
      magnet: '',
      roomValid: false,
      showTorrent: false
    }
  }
}
</script>
<style scoped lang="scss">
.landing {
  min-width: 45em;
}

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

#videoPlayer {
  min-width: 100%;
  min-height: 100%;

  width: 100%;
  height: 100%;

  position: relative;
  display: table-cell;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
}

#videoSidebar {
  display: table-cell;
  width: 20em;
  height: 100%;
  background-color: $color-primary-dark;
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
