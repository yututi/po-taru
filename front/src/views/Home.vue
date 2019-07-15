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
    <template v-slot:menu>
      <card clickable v-ripple @click="show=true">RSS設定</card>
      <card clickable v-ripple @click="logout">Logout</card>
    </template>
  </layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Layout from "@/views/Layout.vue";
import { authModule } from "@/stores";
import axios from "axios";

@Component({
  components: {
    Layout,
    Card: () => import("@/components/Card.vue"),
    RssConfigDialog: () => import("@/components/RSSConfigDialog.vue")
  }
})
export default class Home extends Vue {
  show: boolean = false;
  routes: Array<{ name: string; path: string; iconClasses: String[] }> = [
    {
      name: "RSS Feed",
      path: "rss",
      iconClasses: ["fas", "fa-rss"]
    }
  ];
  logout() {
    authModule.logout().then(() => {
      this.$router.push("/login");
    });
  }
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
  align-items: center;

  &__text {
    flex: 1;
    font-weight: 300;
  }
}
</style>
