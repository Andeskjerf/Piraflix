<template>
  <div>
    <video id="videoPlayer" autoplay></video>
    <div id="videoSidebarContainer">
      <sidebar-content :roomId="roomId" />
    </div>
  </div>
</template>

<script>
import { Room } from '@/api/models/RoomModel'
import SidebarContent from './SidebarContent.vue'
import { getRoom } from '@/api/RoomAPI'

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

      this.buffering = false
      console.log('noEmitSeek:', this.noEmitSeek)
      if (this.paused || (this.noEmitSeek)) {
        this.isSeeking = false
        this.noEmitPlayback = false
        this.noEmitSeek = false
      }
    })

    this.player.addEventListener('seeking', () => {
      console.log('"seeking" event fired')
      // console.log('Paused: ', this.paused)
      if (this.overrideIsSeeking) {
        this.isSeeking = false
        this.overrideIsSeeking = false
      } else if (!this.paused) {
        this.isSeeking = true
        this.buffering = true
      }
      if (!this.noEmitSeek) {
        this.$socket.client.emit('seeked', { roomId: this.room.id, timestamp: this.player.currentTime })
      }
      clearTimeout(this.idSeekTest)
    })

    this.player.onplaying = (event) => {
      console.log('Buffering complete')
    }

    this.player.onwaiting = (event) => {
      console.log('Buffering...')
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
      console.log('Buffering:', this.buffering)
      if (!this.buffering) {
        this.isSeeking = false
        this.noEmitPlayback = false
      }
    }
  },
  components: {
    SidebarContent
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
  display: table-cell;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
}
#videoSidebarContainer {
  display: table-cell;
  width: 20em;
  height: 100%;
  background-color: $color-primary-dark;
  vertical-align: bottom;
}

</style>
