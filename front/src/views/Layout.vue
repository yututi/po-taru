<template>
  <div class="app" @click="hideNavSp">
    <header class="app__header header">
      <a class="header__icon" @click.prevent.stop="toggleNav">
        <i class="fas fa-bars"></i>
      </a>
      <div class="header__title">
        <span @click="$router.push('/')">{{appname}}</span>
      </div>
      <a v-if="$slots.menu" class="header__right-items">
        <app-menu :show.sync="showMenu">
          <template v-slot:activator>
            <i class="header__icon fas fa-cog" @click="showMenu = true"></i>
          </template>
          <template v-slot:menu>
            <slot name="menu" />
          </template>
        </app-menu>
      </a>
    </header>
    <nav @click.stop class="app__sidenav sidenav" :class="navCls">
      <slot name="nav" />
    </nav>
    <div class="app__body">
      <slot name="content" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {
    AppMenu: () => import("@/components/Menu.vue"),
    Card: () => import("@/components/Card.vue")
  }
})
export default class Layout extends Vue {
  appname: string = process.env.VUE_APP_TITLE;
  showNav: boolean = true;
  showNavSp: boolean = false;
  showMenu: boolean = false;

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
