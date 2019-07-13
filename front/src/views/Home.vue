<template>
  <layout>
    <template v-slot:nav>
      <div class="home-nav">
        <router-link
          class="home-nav__item nav-link"
          v-for="pathConfig in routes"
          :key="pathConfig.name"
          tag="button"
          :to="pathConfig.path"
          v-ripple
        >
          <i class="nav-link__icon" :class="pathConfig.iconClasses"></i>
          <div class="nav-link__text">{{pathConfig.name}}</div>
        </router-link>
      </div>
    </template>
    <template v-slot:content>
      <div class="home">
        <router-view></router-view>
      </div>
    </template>
  </layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Layout from "@/views/Layout.vue";
import RSSReader from "@/components/RSSReader.vue";
import axios from "axios";

@Component({
  components: {
    Layout,
    "rss-reader": RSSReader
  }
})
export default class Home extends Vue {
  routes: Array<{ name: string; path: string; iconClasses: String[] }> = [
    {
      name: "RSS Feed",
      path: "rss",
      iconClasses: ["fas", "fa-rss"]
    }
  ];
}
</script>
<style lang="stylus">
@require '../styles/palette.styl';

.home-nav {
  display: flex;
  flex-direction: column;
  color: $primary;

  &__item {
  }
}

.nav-link {
  display: flex;
  font-size: 2em;
  padding: 0.5em 1em;
  user-select: none;
  outline: 0;

  &__text {
    flex: 1;
    font-weight: 700;
  }
}
</style>
