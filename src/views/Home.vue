<template>
  <transition name="slide-fade" mode="out-in" @after-leave="renderVideo">
    <video-player
      v-if="showTorrent"
      id="videoPlayerContainer"
      :room="room"
      :watch-video="showTorrent"
      @close-video="leaveRoom"
    ></video-player>
    <div v-else class="landing">
      <logo id="logo"></logo>
      <div class="center">
        <room-creation-box
          :magnet="inputText"
          @magnet-link="checkMagnetLink"
        ></room-creation-box>
        <big-button
          text="Host room"
          :active="roomValid"
          :style="buttonStyle"
          @clicked="createRoom"
        ></big-button>
      </div>
      <div id="footer"></div>
    </div>
  </transition>
</template>

<script lang="ts">
import Logo from "@/components/Logo.vue";
import BigButton from "@/components/CustomButton.vue";
import RoomCreationBox from "@/components/RoomCreationBox.vue";
import VideoPlayer from "@/components/VideoPlayer.vue";
import { createRoom, getRoom } from "@/api/RoomAPI";
import { Room } from "@/api/models/RoomModel";
import { defineComponent } from "vue";
import WebTorrent, { Torrent } from "webtorrent";

const client = new WebTorrent();
// let socket: Socket | undefined;
// let roomId: string | undefined;

// window.onerror = function () {
//   if (client.torrents.length > 0) {
//     const torrent: Torrent = client.torrents[0];

//     const file = torrent.files.find(function (file) {
//       return file.name.endsWith(".mp4");
//     });
//     if (file !== undefined) {
//       console.log(torrent.downloadSpeed);
//       torrent.resume();
//       console.log(torrent.progress, torrent.paused);

//       console.log(file.progress);

//       file.renderTo("video#videoPlayer");
//       socket?.emit("join", { roomId: roomId });
//     } else {
//       console.log("Error while getting file data from torrent!");
//       // this.leaveRoom();
//       client.destroy((err: string | Error) => console.log(err));
//     }
//   }
// };

client.on("error", (err: any) => {
  console.log("Something went wrong while torrenting");
  console.log(err);
});

export default defineComponent({
  name: "Home",
  components: {
    Logo,
    RoomCreationBox,
    BigButton,
    VideoPlayer,
  },
  data() {
    return {
      inputText: "",
      roomValid: false,
      showTorrent: false,
      magnet: "",
      room: new Room(),
      torrent: {} as Torrent,
      buttonStyle: {
        fontSize: "38px",
        width: "7em",
        height: "2em",
      },
    };
  },

  mounted() {
    // socket = this.$socket.client;

    // this.$socket.$subscribe("join", (roomId: string) => {
    //   if (roomId.length > 0) {
    //     getRoom(roomId)
    //       .then((room: Room) => {
    //         if (room.id !== "-1") {
    //           this.joinRoom(room);
    //         } else {
    //           this.createRoom();
    //         }
    //       })
    //       .catch((err) => {
    //         console.log(err);
    //       });
    //   }
    // });

    // client.on("error", (err: string | Error) => {
    //   console.log(err);
    //   this.leaveRoom();
    // });

    // client.on("torrent", (torrent: Torrent) => {
    //   console.log(torrent);
    // });

    const path = this.$route.path.substr(1);
    if (path.length > 0) {
      getRoom(path)
        .then((room: Room) => {
          if (room.id !== "-1") {
            this.joinRoom(room);
          } else {
            console.log("No room found with this ID");
            history.pushState(null, "", "/");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
  beforeUnmount() {
    if (this.room !== null) {
      this.$socket.client.emit("leave", { roomId: this.room.id });
    }
  },
  methods: {
    createRoom: async function (): Promise<void> {
      const room = await createRoom(this.magnet);
      if (room.id !== "-1") {
        this.joinRoom(room);
      } else {
        console.log("Invalid room ID");
      }
    },

    checkMagnetLink: function (value: string): void {
      const isMagnetLink = value.includes("magnet:?xt=urn:btih:");
      if (isMagnetLink && !this.roomValid) {
        this.roomValid = true;
        this.magnet = value;
      } else if (!isMagnetLink && this.roomValid) {
        this.roomValid = false;
        this.magnet = value;
      }
    },

    joinRoom: function (room: Room): void {
      console.log("Joining room " + room.id);
      history.pushState(null, "", room.id);
      this.room = room;

      this.roomValid = false;
      this.showTorrent = true;
    },

    leaveRoom: function (): void {
      history.pushState(null, "", "/");
      this.magnet = "";
      this.room = new Room();
      this.roomValid = false;
      this.showTorrent = false;
      this.torrent.destroy();
      this.$socket.client.emit("leave");
    },

    renderVideo(): void {
      // console.log("RENDER");
      if (this.room.id !== "-1") {
        // roomId = this.room.id;
        // client.add(this.room.magnet);
        client.add(this.room.magnet, (torrent: Torrent) => {
          this.torrent = torrent;
          const file = torrent.files.find(function (file) {
            return file.name.endsWith(".mp4");
          });
          if (file !== undefined) {
            file.renderTo("video#videoPlayer");
          } else {
            console.log("Error while getting file data from torrent!");
            this.leaveRoom();
          }
        });
        this.$socket.client.emit("join", { roomId: this.room.id });
      }
    },
  },
});
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
