<template>
  <div class="app" @click="hideNav()">
    <div class="app__header header">
      <a class="header__left-menu" href="#" @click.prevent.stop="toggleNav">
        <i class="fas fa-hamburger"></i>
      </a>
      <span>{{appname}}</span>
      <div class="header__right-menu"></div>
    </div>
    <nav click.prevent.stop class="app__sidenav" :class="navCls">aa</nav>
    <div class="app__body">
      <slot name="content"/>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src

@Component({
  components: {
    HelloWorld
  }
})
export default class Layout extends Vue {
  appname: string = "sample";
  showNav: boolean = true;
  showNavSp: boolean = false;

  get navCls() {
    return {
      "app__sidenav--show-pc": this.showNav,
      "app__sidenav--show-sp": this.showNavSp
    };
  }

  toggleNav() {
    this.showNav = !this.showNav;
    this.showNavSp = true;
  }
  hideNav() {
    this.showNavSp = false;
  }

  mounted() {}
}
</script>
<style lang="stylus">
@require '../styles/index.styl';
</style>
