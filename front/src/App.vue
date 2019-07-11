<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { authModule } from "./stores";

@Component({})
export default class App extends Vue {
  created() {
      authModule.getUserInfo();
  }
}
</script>

<style lang="stylus">
#app {
  font-family: Roboto, 'Noto Sans CJK JP', 'Noto Sans JP', Arial, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
