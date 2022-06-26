/* eslint-disable no-var */
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faFilmAlt,
  faMagnet,
  faUnlink,
  faUsers,
  faCog,
} from "@fortawesome/pro-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import "@fontsource/bebas-neue";
import "@fontsource/open-sans";
import VueSocketIOExt from "vue-socket.io-extended";
import config from "../config/hosts.json";
import { checkCookie } from "@/api/CookieAPI";
import { getUserData } from "@/api/UserAPI";
import * as browserfs from "browserfs";
import "fs";

library.add(faFilmAlt);
library.add(faMagnet);
library.add(faUnlink);
library.add(faUsers);
library.add(faCog);

browserfs.install(window);
browserfs.configure(
  {
    fs: "LocalStorage",
    options: {},
  },
  function (e) {
    if (e) {
      throw e;
    }
  },
);

checkCookie()
  .then(async () => {
    var user = await getUserData();

    const socket = (await import("socket.io-client")).io(
      config.httpType + "://" + config.ip + ":" + config.backendPort,
      { withCredentials: true },
    );

    const app = createApp(App)
      .component("font-awesome-icon", FontAwesomeIcon)
      .use(store)
      .use(router)
      .use(VueSocketIOExt, socket)
      .provide("userData", user);

    app.mount("#app");
  })
  .catch((error) => {
    console.log("Error while getting cookie!");
    console.log(error);
  });
