<template>
  <div>
    <div id="videoContainer">
      <video id="videoPlayer" autoplay></video>
      <transition name="fade">
        <div v-if="bufferingUsers.length > 0" id="videoOverlay">
          <div id="overlayBuffering">
            <div id="bufferingUser" v-for="user in bufferingUsers" :key="user.identifier">
              <Avatar id="chatAvatar" :name=user.username />
              <div>
                <p id="username">{{ user.username }}</p>
                <p class="statusMessage">Buffering...</p>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
    <div id="videoSidebarContainer">
      <sidebar-content :roomId="roomId" />
    </div>
  </div>
</template>

<script>
import { Room } from '@/api/models/RoomModel'
import SidebarContent from './SidebarContent.vue'
import { getRoom } from '@/api/RoomAPI'
import Avatar from 'vue-boring-avatars'

export default {
  props: { room: Room },
  sockets: {
    beginPlay () {
      console.log('PLAY')
      this.noEmitPlayback = true
      this.playVideo()
    },
    pausePlay () {
      console.log('PAUSE')
      this.noEmitPlayback = true
      this.player.pause()
    },
    seek (data) {
      console.log('SEEK')
      this.noEmitSeek = true
      this.player.currentTime = data.time
    },
    buffering (data) {
      var parsed = JSON.parse(data)
      this.bufferingUsers = []
      for (var item of parsed) {
        const obj = {
          identifier: item.identifier,
          username: item.username
        }
        var result = this.bufferingUsers.find(({ identifier }) => identifier === item.identifier)
        if (result === undefined) {
          console.log(obj)
          console.log(item)
          this.bufferingUsers.push(obj)
        }
      }

      // if (this.bufferingUsers.length > 0) {
      //   this.noEmitPlayback = true
      //   console.log('Waiting for users to buffer...')
      //   this.player.pause()
      // } else if (!this.paused) {
      //   console.log('All users buffered, resuming playback')
      //   this.playVideo()
      // }
    }
  },
  mounted () {
    this.player = document.querySelector('video')

    this.player.addEventListener('loadedmetadata', () => {
      this.initVideo()
    })

    this.player.addEventListener('play', () => {
      console.log('"play" event fired')
      this.idSeekTest = setTimeout(function () {
        console.log('noEmitPlayback: ', this.noEmitPlayback, 'isSeeking', this.isSeeking)
        if (!this.noEmitPlayback && !this.isSeeking) {
          console.log('Play triggered')
          this.paused = false
          this.$socket.client.emit('play', this.room.id)
        }

        this.resetNoEmit()
      }.bind(this), this.SEEKEVENT_TIMEOUT)
    })

    this.player.addEventListener('pause', () => {
      console.log('"pause" event fired')
      this.idSeekTest = setTimeout(function () {
        console.log('noEmitPlayback: ', this.noEmitPlayback, 'isSeeking', this.isSeeking)
        if (!this.noEmitPlayback && !this.isSeeking) {
          console.log('Pause triggered')
          this.paused = true
          this.$socket.client.emit('pause', this.room.id)
        }

        this.resetNoEmit()
      }.bind(this), this.SEEKEVENT_TIMEOUT)
    })

    this.player.addEventListener('timeupdate', () => {
      this.$socket.client.emit('timestamp', { roomId: this.room.id, timestamp: this.player.currentTime })
    })

    this.player.addEventListener('seeked', () => {
      console.log('"seeked" event fired', this.noEmitSeek)

      console.log('noEmitSeek:', this.noEmitSeek)
      if (this.paused || (this.noEmitSeek)) {
        this.isSeeking = false
        this.noEmitPlayback = false
        this.noEmitSeek = false
      }
    })

    this.player.addEventListener('seeking', () => {
      console.log('"seeking" event fired')
      if (this.overrideIsSeeking) {
        this.isSeeking = false
        this.overrideIsSeeking = false
      } else if (!this.paused) {
        this.isSeeking = true
      }
      if (!this.noEmitSeek) {
        this.$socket.client.emit('seeked', { roomId: this.room.id, timestamp: this.player.currentTime })
      }
      clearTimeout(this.idSeekTest)
    })

    this.player.onplaying = (event) => {
      if (this.buffering) {
        console.log('Buffering complete')
        this.buffering = false
        this.$socket.client.emit('bufferComplete', this.room.id)
      }
    }

    this.player.onwaiting = (event) => {
      console.log('Buffering...')
      this.buffering = true
      this.$socket.client.emit('buffering', this.room.id)
    }
  },
  methods: {
    async playVideo () {
      var promise = this.player.play()
      if (promise !== undefined) {
        promise
          .then(_ => {
            // console.log('Autoplayed')
          })
          .catch(_ => {
            console.log('Autoplay disallowed, muting')
            this.player.muted = true
            this.player.play()
          })
      }

      return true
    },
    async initVideo () {
      var room = await getRoom(this.room.id)
      this.roomId = this.room.id
      console.log(room)
      console.log(this.roomId, this.room.paused)
      console.log(this.room.paused ? 'Room is paused' : 'Room is playing')
      this.paused = this.room.paused
      this.overrideIsSeeking = true
      this.player.currentTime = room.timestamp

      if (!this.paused) {
        this.playVideo()
      }
    },
    resetNoEmit () {
      this.isSeeking = false
      this.noEmitPlayback = false
    }
  },
  components: {
    SidebarContent,
    Avatar
  },
  data () {
    return {
      roomId: this.room?.id,
      overrideIsSeeking: false,
      isSeeking: false,
      idSeekTest: null,
      noEmitSeek: false,
      noEmitPlayback: false,
      paused: false,
      buffering: false,
      bufferingUsers: [],
      SEEKEVENT_TIMEOUT: 30
    }
  }

}
</script>
<style lang="scss" scoped>

#videoPlayer {
  min-width: 100%;
  min-height: 100%;

  width: 100%;
  height: 100%;

  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  z-index: 0;
}

#videoContainer {
  position: relative;
  display: table-cell;
}

#videoOverlay {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
  top: 0px;
  right: 0px;

  width: 100%;
  height: 100%;

  pointer-events: none;
}

#overlayBuffering {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.75);
  opacity: 1;
  z-index: 1;
  top: 0px;
  right: 0px;

  max-width: 300px;
  min-width: 200px;

  width: 25%;
  height: 100%;
}

#videoSidebarContainer {
  display: table-cell;
  width: 20em;
  height: 100%;
  background-color: $color-primary-dark;
  vertical-align: bottom;
}

#chatAvatar {
  align-self: center;
}

#bufferingUser {
  display: inline-flex;
  margin: 1em;

  div > p {
    padding: 0.25em 0.0em 0.0em 1em;
    margin: 0;
    color: $color-text;
  }
}

#username {
  font-weight: bold;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

</style>
