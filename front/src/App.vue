<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { authModule } from "./stores/auth";

@Component
export default class App extends Vue {
  created() {
    //   authModule.getUserInfo();
  }
}
</script>

<style lang="stylus">
@import url('https://fonts.googleapis.com/css?family=Noto+Sans+JP:300&display=swap');

#app {
  font-family: Roboto, 'Noto Sans JP', 'Noto Sans JP', Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
