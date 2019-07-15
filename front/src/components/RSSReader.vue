<template>
  <div class="rss-reader">
    <expansion-panel id="test" title="hoge">
      <template v-slot:body>
        <div class="articles">
          <article-card
            class="articles__item"
            v-for="(info, index) in soterdAtricles"
            :key="title + index.toString()"
            :article="info"
          />
        </div>
      </template>
    </expansion-panel>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import ExpansionPanel from "@/components/ExpansionPanel.vue";
import ArticleCard from "@/components/ArticleCard.vue";
import { authModule } from "@/stores";
import { query4Text, query4TextFromDoc } from "@/utlis";
import axios from "axios";
import { ArticleInfo } from "@/dto";

@Component({
  components: {
    ExpansionPanel,
    ArticleCard
  }
})
export default class RSSReader extends Vue {
  articles: ArticleInfo[] = [];

  _cancelId!: number;

  async updateList() {
    const response = await axios.post(`rss`);
    console.log(response.data);
    this.articles = response.data.map(
      (r: Partial<ArticleInfo>) =>
        new ArticleInfo(r.rssId, r.siteName, r.updated, r.title, r.link, r.img)
    );
  }
  get soterdAtricles(): ArticleInfo[] {
    return this.articles.sort((prev, next) => {
      return next.updatedDate.getTime() - prev.updatedDate.getTime();
    });
  }
  mounted() {
    this.updateList();
    this._cancelId = setInterval(() => {
      this.updateList();
    }, 60 * 1000);
  }
  beforeDestroy() {
    clearInterval(this._cancelId);
  }
}
</script>
<style lang="stylus">
@require '../styles/rss.styl';

.articles {
  padding: 5px;

  &__item {
    & + & {
      margin-top: 5px;
    }
  }
}
</style>
