module.exports = {
  css: {
    loaderOptions: {
      sass: {
        prependData: `
            @import "@/styles/global.scss";
          `
      }
    }
  },
  configureWebpack: {
    devtool: 'source-map'
  }
}
