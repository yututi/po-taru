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
      <card clickable v-ripple @click="logout">ログアウト</card>
    </template>
  </layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Layout from "@/views/Layout.vue";
import { authModule } from "@/stores/auth";
import axios from "axios";

@Component({
  components: {
    Layout,
    Card: () => import("@/components/Card.vue")
  }
})
export default class Home extends Vue {
  show: boolean = false;
  routes: Array<{ name: string; path: string; iconClasses: String[] }> = [
    {
      name: "RSSフィード",
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

.home {
  height: 100%;
  margin: 0px;
}

.nav-link {
  display: flex;
  font-size: 28px;
  padding: 0.5em 0.5em;
  user-select: none;
  outline: 0;
  align-items: center;

  &__text {
    flex: 1;
    font-weight: 300;
    white-space: nowrap;
  }
}
</style>
