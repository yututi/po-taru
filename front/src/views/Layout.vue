<template>
  <div class="app" @click="hideNavSp">
    <header class="app__header header progress-bar" :class="headerClasses">
      <a class="header__icon" @click.prevent.stop="toggleNav">
        <i class="fas fa-bars"></i>
      </a>
      <div class="header__title">
        <span @click="$router.push('/')">{{appname}}</span>
      </div>
      <a v-if="$slots.menu">
        <icon-menu style="margin-right:10px;" position="bottom-left" :hideOnOtherClick="true">
          <slot name="menu" />
        </icon-menu>
      </a>
    </header>
    <nav class="app__sidenav sidenav" :class="navCls">
      <slot name="nav" />
    </nav>
    <div class="app__body">
      <slot name="content" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import IconMenu from "@/components/IconMenu.vue";
import { globalModule } from "@/stores/global";

@Component({
  components: {
    AppMenu: () => import("@/components/Menu.vue"),
    Card: () => import("@/components/Card.vue"),
    ModalDialog: () => import("@/components/ModalDialog.vue"),
    IconMenu
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

  get headerClasses() {
    return { "header--progress": globalModule.isLoading };
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

.info-msgs {
  position: absolute;
  width: 100%;

  .info-msg {
    margin: 5px auto;
    width: fit-content;
    min-width: 200px;
    text-align: center;
    background-color: $primary;
    color: $primaryText;
    padding: 1em;
    border-radius: 5px;
    transition: all 0.3s;
    animation: showMsg 0.5s 0.1s 1;
    overflow: hidden;
    opacity: 0;

    &--show {
      opacity: 1;
    }
  }
}

@keyframes showMsg {
  0% {
    height: 0px;
  }

  100% {
    height: 100%;
  }
}
</style>
