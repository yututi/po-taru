<template>
  <div class="rss-reader">
    <div class="articles">
      <article-card
        class="articles__item"
        v-for="(info, index) in soterdAtricles"
        :key="title + index.toString()"
        :article="info"
      />
      <a
        class="articles__sticky-icon"
        v-ripple
        @click="showDialog = true"
        @mouseenter="lazyLoad=true"
      >
        <i class="app-icon fas fa-cog"></i>
      </a>
    </div>
    <rss-config-dialog v-if="lazyLoad" v-model="showDialog" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import ArticleCard from "@/components/ArticleCard.vue";
import IconMenu from "@/components/IconMenu.vue";
import axios from "axios";
import { ArticleInfo } from "@/dto";
import { articleModule } from "@/stores/article";

@Component({
  components: {
    ArticleCard,
    IconMenu,
    "rss-config-dialog": () => import("@/components/RSSConfigDialog.vue")
  }
})
export default class RSSReader extends Vue {
  _cancelId!: number;
  lazyLoad: boolean = false;
  showDialog: boolean = false;

  get soterdAtricles(): ArticleInfo[] {
    return articleModule.soterdAtricles;
  }
  mounted() {
    articleModule.updateList();
    this._cancelId = setInterval(() => {
      articleModule.updateList();
    }, 60 * 1000);
  }
  beforeDestroy() {
    clearInterval(this._cancelId);
  }
}
</script>
<style lang="stylus">
@require '../styles/rss.styl';
@require '../styles/palette.styl';

.articles {
  padding: 5px;

  &__item {
    background-color: white;

    & + & {
      margin-top: 5px;
    }
  }

  &__sticky-icon {
    position: fixed;
    right: 20px;
    bottom: 20px;
    background-color: white;
    border-radius: 50%;
    border: 1px solid gainsboro;
    box-sizing: border-box;
    cursor: pointer;
    color:$accent;
  }
}
</style>
