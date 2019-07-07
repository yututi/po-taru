<template>
  <div class="app" @click="hideNavSp">
    <header class="app__header header">
      <a class="header__left-menu" href="#" @click.prevent.stop="toggleNav">
        <i class="fas fa-hamburger"></i>
      </a>
      <span>{{appname}}</span>
      <div class="header__right-menu"></div>
    </header>
    <nav @click.stop class="app__sidenav sidenav" :class="navCls">
      <slot name="nav"/>
    </nav>
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
    if (window.innerWidth < 770) {
      this.showNavSp = true;
    } else {
      this.showNav = !this.showNav;
    }
  }
  hideNavSp() {
    this.showNavSp = false;
  }
  handleResize(e: Event) {
    if (window.innerWidth < 770) {
      this.showNavSp = false;
    }
  }
  mounted() {
    window.addEventListener("resize", this.handleResize);
  }
  destroy() {
    window.removeEventListener("resize", this.handleResize);
  }
}
</script>
<style lang="stylus">
@require '../styles/index.styl';
</style>
