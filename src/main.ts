import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faFilmAlt, faMagnet, faUnlink } from '@fortawesome/pro-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import '@fontsource/source-sans-pro'
import '@fontsource/bebas-neue'
import '@fontsource/open-sans'
import LoadScript from 'vue-plugin-load-script'
import VueSocketIOExt from 'vue-socket.io-extended'
import { io } from 'socket.io-client'

library.add(faFilmAlt)
library.add(faMagnet)
library.add(faUnlink)

const socket = io('http://192.168.1.107:5000')

const app = createApp(App)
  .component('font-awesome-icon', FontAwesomeIcon)
  .use(store)
  .use(router)
  .use(LoadScript)
  .use(VueSocketIOExt, socket)

app.mount('#app')
