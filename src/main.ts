/* eslint-disable no-var */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faFilmAlt, faMagnet, faUnlink, faUsers, faCog } from '@fortawesome/pro-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import '@fontsource/source-sans-pro'
import '@fontsource/bebas-neue'
import '@fontsource/open-sans'
import LoadScript from 'vue-plugin-load-script'
import VueSocketIOExt from 'vue-socket.io-extended'
import { io } from 'socket.io-client'
import config from '../config/hosts.json'
import { checkCookie } from './api/CookieAPI'
import { getUserData } from './api/UserAPI'

library.add(faFilmAlt)
library.add(faMagnet)
library.add(faUnlink)
library.add(faUsers)
library.add(faCog)

checkCookie()
  .then(async () => {
    var user = await getUserData()

    const socket = io(config.httpType + '://' + config.ip + ':' + config.backendPort,
      { withCredentials: true })

    const app = createApp(App)
      .component('font-awesome-icon', FontAwesomeIcon)
      .use(store)
      .use(router)
      .use(LoadScript)
      .use(VueSocketIOExt, socket)
      .provide('userData', user)

    app.mount('#app')
  })
  .catch((error) => {
    console.log('Error while getting cookie!')
    console.log(error)
  })
