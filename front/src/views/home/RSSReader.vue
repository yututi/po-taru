<template>
  <div class="rss-reader" @scroll="onScroll">
    <div class="rss-filters tags">
      <div
        class="tags__item tag"
        v-for="site in displaySites"
        :class="{'tag--disable':site.isIgnoreRequired}"
        :key="site.id"
        @click="toggleFilter(site)"
      >{{site.site_name}}</div>
    </div>
    <div class="articles">
      <div
        class="articles__item"
        v-for="(info, index) in soterdArticles"
        :key="info.site + index.toString()"
      >
        <article-card :article="info" />
      </div>
    </div>
    <icon-menu class="articles__sticky-icon" ref="config">
      <rss-config-form @submit="$refs.config.hideMenu()" />
    </icon-menu>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import ArticleCard from "@/components/ArticleCard.vue";
import IconMenu from "@/components/IconMenu.vue";
import { ArticleInfo, SiteInfo } from "@/dto";
import { articleModule } from "@/stores/article";
import { globalModule } from "@/stores/global";

@Component({
  components: {
    ArticleCard,
    IconMenu,
    "rss-config-dialog": () => import("@/components/RSSConfigDialog.vue"),
    "rss-config-form": () => import("@/components/RSSConfigForm.vue")
  }
})
export default class RSSReader extends Vue {
  _cancelId!: number;
  _debounceId!: number;
  lazyLoad: boolean = false;
  showDialog: boolean = false;
  showMenu: boolean = false;

  get soterdArticles(): ArticleInfo[] {
    return articleModule.displayArticles;
  }

  get displaySites() {
    return articleModule.displaySites;
  }

  onScroll({ target }: Event) {
    const el = target as HTMLElement;
    if (el.scrollTop + el.clientHeight >= el.scrollHeight - 1) {
      clearTimeout(this._debounceId);
      this._debounceId = setTimeout(() => {
        articleModule.nextArticles();
      }, 50);
    }
  }

  toggleFilter(site: SiteInfo) {
    site.isIgnoreRequired = !site.isIgnoreRequired;
    articleModule.updateArticles();
  }

  mounted() {
    articleModule.initArticles();
    this._cancelId = setInterval(() => {
      articleModule.updateArticles();
    }, 60 * 1000);
  }
  beforeDestroy() {
    clearInterval(this._cancelId);
  }
}
</script>
<style lang="stylus">
@require '../../styles/rss.styl';
@require '../../styles/palette.styl';
@require '../../styles/base.styl';

.tags {
  display: flex;
  padding-top: 5px;
  padding-left: 5px;

  &__item {
    margin-top: 5px;
    margin-left: 5px;
  }
}

.tag {
  font-size: 12px;
  background-color: $accent;
  color: $accentText;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;

  &--disable {
    background-color: $disable;
  }
}

.articles {
  padding: 5px;
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;

  &__item {
    +pc() {
      max-width: 50%;
      flex-basis: 50%;
    }

    +sp() {
      max-width: 100%;
      flex-basis: 100%;
    }

    +ws() {
      max-width: 33.333%;
      flex-basis: 33.333%;
    }

    box-sizing: border-box;
    padding: 5px;
  }

  &__sticky-icon {
    position: fixed;
    right: 20px;
    bottom: 20px;
  }
}
</style>
