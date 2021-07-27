module.exports = {
  css: {
    loaderOptions: {
      sass: {
        prependData: `
            @import "@/styles/global.scss";
            @import "@/styles/loader.scss";
          `
      }
    }
  },
  configureWebpack: {
    devtool: 'source-map'
  }
}
