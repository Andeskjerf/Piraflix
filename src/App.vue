<template>
  <body id="body">
    <router-view />
  </body>
</template>

<style lang="scss">
@font-face {
  font-family: 'BebasNeue';
  src: url(~@/fonts/BebasNeue.otf);
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

html {
  background-color: #142850;
  width: 100%;
  height: 100%;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
