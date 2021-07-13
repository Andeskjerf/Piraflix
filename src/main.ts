import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faFilmAlt, faMagnet, faUnlink } from '@fortawesome/pro-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import '@fontsource/source-sans-pro'
import '@fontsource/bebas-neue'
import LoadScript from 'vue-plugin-load-script'
import VueSocketIO from 'vue-socket.io'

library.add(faFilmAlt)
library.add(faMagnet)
library.add(faUnlink)

const app = createApp(App)
  .component('font-awesome-icon', FontAwesomeIcon)
  .use(store)
  .use(router)
  .use(LoadScript)
  .use(new VueSocketIO({
    debug: true,
    connection: 'http://127.0.0.1:5000'
  }))

app.mount('#app')
