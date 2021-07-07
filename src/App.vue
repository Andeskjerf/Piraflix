<template>
  <body id="body">
    <router-view />
  </body>
</template>

<style lang="scss">
html {
    background-color: $color-background;
    width: 100%;
    height: 100%;
}
* {
    font-family: $font;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
</style>
