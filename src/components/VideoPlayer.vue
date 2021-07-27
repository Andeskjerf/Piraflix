<template>
  <div>
    <div id="videoContainer">
      <transition name="fade">
        <video v-show="!loadingVideo" id="videoPlayer" autoplay />
      </transition>
      <div id="videoOverlay">
        <a v-on:click.self="leaveRoom" id="closeButton" />
        <transition name="fade">
          <div v-if="loadingVideo" id="loadingOverlay">
            <div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
          </div>
        </transition>
        <transition name="fade">
          <div v-if="bufferingUsers.length > 0">
            <div class="boxShadow" id="overlayBuffering">
              <transition-group name="itemAnim" tag="div">
                <div id="bufferingUser" v-for="user in bufferingUsers" :key="user">
                  <Avatar id="chatAvatar" :name=user.username />
                  <div>
                    <p id="username">{{ user.username }}</p>
                    <p class="statusMessage">Buffering...</p>
                  </div>
                </div>
              </transition-group>
            </div>
          </div>
        </transition>
      </div>
    </div>
    <sidebar-content id="videoSidebarContainer" :roomId="roomId" />
  </div>
</template>

<script lang="ts">
import { Room } from '@/api/models/RoomModel'
import SidebarContent from './SidebarContent.vue'
import { getRoom } from '@/api/RoomAPI'
import Avatar from 'vue-boring-avatars'
import { defineComponent } from 'vue'
import { UserModel } from '@/api/models/UserModel'

export default defineComponent({
  props: {
    room: Room,
    watchVideo: Boolean
  },
  sockets: {
    beginPlay (): void {
      console.log('PLAY')
      this.noEmitPlayback = true
      this.playVideo()
    },
    pausePlay (): void {
      console.log('PAUSE')
      this.noEmitPlayback = true
      this.pauseVideo()
    },
    seek (data): void {
      console.log('SEEK')
      this.noEmitSeek = true
      this.seekVideo(data.time)
    },
    buffering (data): void {
      var parsed = JSON.parse(data)
      var newBufferingUsers: UserModel[] = []

      var i = 0
      for (var item of parsed) {
        const obj: UserModel = {
          identifier: item.identifier,
          username: item.username,
          index: i
        }

        newBufferingUsers.push(obj)
        i += 1
      }

      for (const user of newBufferingUsers) {
        const res = this.bufferingUsers.findIndex(x => x.identifier === user.identifier)
        if (res === -1) {
          this.bufferingUsers.push(user)
        }
      }

      this.bufferingUsers = this.bufferingUsers.filter((value) => {
        return newBufferingUsers.findIndex(x => x.identifier === value.identifier) !== -1
      })
    }
  },
  mounted (): void {
    const player = this.getPlayer()
    if (player !== null) {
      player.onloadedmetadata = () => {
        this.initVideo()
      }

      player.onplay = () => {
        console.log('"play" event fired')
        this.idSeekTest = setTimeout(() => {
          console.log('noEmitPlayback: ', this.noEmitPlayback, 'isSeeking', this.isSeeking)
          if (!this.noEmitPlayback && !this.isSeeking) {
            console.log('Play triggered')
            this.paused = false
            this.$socket.client.emit('play', this.getRoom().id)
          }

          this.resetNoEmit()
        }, this.SEEKEVENT_TIMEOUT)
      }

      player.onpause = () => {
        console.log('"pause" event fired')
        this.idSeekTest = setTimeout(() => {
          console.log('noEmitPlayback: ', this.noEmitPlayback, 'isSeeking', this.isSeeking)
          if (!this.noEmitPlayback && !this.isSeeking) {
            console.log('Pause triggered')
            this.paused = true
            this.$socket.client.emit('pause', this.getRoom().id)
          }

          this.resetNoEmit()
        }, this.SEEKEVENT_TIMEOUT)
      }

      player.ontimeupdate = () => {
        this.$socket.client.emit('timestamp', { roomId: this.getRoom().id, timestamp: this.getCurrentTimestamp() })
      }

      player.onseeked = () => {
        console.log('"seeked" event fired', this.noEmitSeek)

        console.log('noEmitSeek:', this.noEmitSeek)
        if (this.paused || (this.noEmitSeek)) {
          this.isSeeking = false
          this.noEmitPlayback = false
          this.noEmitSeek = false
        }
      }

      player.onseeking = () => {
        console.log('"seeking" event fired')
        if (this.overrideIsSeeking) {
          this.isSeeking = false
          this.overrideIsSeeking = false
        } else if (!this.paused) {
          this.isSeeking = true
        }
        if (!this.noEmitSeek) {
          this.$socket.client.emit('seeked', { roomId: this.getRoom().id, timestamp: this.getCurrentTimestamp() })
        }
        clearTimeout(this.idSeekTest)
      }

      player.onplaying = () => {
        if (this.buffering) {
          console.log('Buffering complete')
          this.buffering = false
          this.$socket.client.emit('bufferComplete', this.getRoom().id)
        }
      }

      player.onwaiting = () => {
        console.log('Buffering...')
        this.buffering = true
        this.$socket.client.emit('buffering', this.getRoom().id)
      }
    }
  },
  methods: {
    playVideo (): void {
      const player = this.getPlayer()
      if (player !== null) {
        var promise = player.play()
        if (promise !== undefined) {
          promise
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            .then(_ => {
            // console.log('Autoplayed')
            })
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            .catch(_ => {
              console.log('Autoplay disallowed, muting')
              player.muted = true
              player.play()
            })
        }
      }
    },
    pauseVideo (): void {
      const player = this.getPlayer()
      if (player !== null) player.pause()
      console.log('Tried to pause but video player is null!')
    },
    seekVideo (time: number): void {
      const player = this.getPlayer()
      if (player !== null) { player.currentTime = time }
      console.log('Tried to seek but video player is null!')
    },
    getCurrentTimestamp (): number {
      const player = this.getPlayer()
      if (player !== null) return player.currentTime
      console.log('Tried to get current timestamp but video player is null!')
      return -1
    },
    async initVideo (): Promise<void> {
      var room = await getRoom(this.getRoom().id)
      this.bufferingUsers = []
      this.roomId = this.getRoom().id
      console.log(this.roomId, room.paused)
      console.log(room.paused ? 'Room is paused' : 'Room is playing')
      this.paused = room.paused
      this.overrideIsSeeking = true
      this.seekVideo(room.timestamp)

      if (!this.paused) { this.playVideo() }
      this.loadingVideo = false
    },
    resetNoEmit (): void {
      this.isSeeking = false
      this.noEmitPlayback = false
    },
    leaveRoom (): void {
      this.noEmitPlayback = true
      this.$emit('closeVideo', false)
    },
    getRoom (): Room {
      if (this.room !== undefined) { return this.room }
      console.log('Room is undefined!')
      return new Room()
    },
    getPlayer (): HTMLMediaElement | null {
      return document.querySelector('video')
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
      idSeekTest: {

      } as any,
      noEmitSeek: false,
      noEmitPlayback: false,
      paused: false,
      loadingVideo: true,
      buffering: false,
      bufferingUsers: {} as UserModel[],
      SEEKEVENT_TIMEOUT: 30
    }
  }

})
</script>
<style lang="scss" scoped>

#videoPlayer {
  min-width: 100%;
  min-height: 100%;

  width: 100%;
  height: 100%;

  position: absolute;
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
  background-color: rgba(0, 0, 0, 0.1);
  z-index: 1;
  top: 0px;
  right: 0px;

  width: 100%;
  height: 100%;

  pointer-events: none;
}

#overlayBuffering {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(20px);
  opacity: 1;
  z-index: 1;
  top: 0px;
  right: 0px;

  max-width: 300px;
  min-width: 250px;

  width: 25%;
  height: 100%;
}

#videoSidebarContainer {
  display: table-cell;
  width: 20em;
  background-color: $color-primary-dark;
  vertical-align: bottom;
  position: relative;
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
  transition: opacity .8s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.itemAnim-item {
  transition: all 0.8s ease;
  display: inline-block;
  margin-right: 10px;
}

.itemAnim-enter-from,
.itemAnim-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.itemAnim-leave-active {
  position: absolute;
}

#closeButton {
  position: absolute;
  top: 32px;
  left: 32px;
  width: 32px;
  height: 32px;
  opacity: 0.7;
  z-index: 3;
  pointer-events: auto;
}

#closeButton:hover {
  opacity: 1;
}

#closeButton:before, #closeButton:after {
  position: absolute;
  left: 15px;
  content: ' ';
  height: 33px;
  width: 2px;
  background-color: $color-text;
}

#closeButton:before {
  transform: rotate(45deg);
}

#closeButton:after {
  transform: rotate(-45deg);
}

#loadingOverlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
}

</style>
