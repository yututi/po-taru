<template>
  <div class="rss-config-form form">
    <div class="form__field">
      <span class="rss-config-label">フィード対象一覧</span>
    </div>
    <div class="form__field rss-config-list">
      <div class="rss-config-list__item" v-for="site in sites" :key="site.id">
        <input type="checkbox" class="checkbox" :id="site.id" v-model="site.isDeleteRequired" />
        <label :for="site.id">{{site.site_name}}</label>
      </div>
    </div>
    <div class="form__action">
      <button class="button" @click="deleteSelectedSites">削除</button>
    </div>

    <div class="form__separator" />
    <div class="form__field">
      <span class="rss-config-label">フィード対象登録</span>
    </div>
    <div class="form__field">
      <text-field type="url" label="URL" v-model="url"></text-field>
    </div>
    <div class="form__action">
      <button class="button" @click="submit">登録</button>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Model, Vue } from "vue-property-decorator";
import TextField from "@/components/TextField.vue";
import Validation from "@/components/Validation.vue";
import { articleModule } from "@/stores/article";
import { authModule } from "../stores/auth";
import { SiteInfo } from "@/dto";
import { globalModule } from "../stores/global";

class CheckableRssInfo {
  constructor(public site: SiteInfo, public isChecked: boolean) {}
}

@Component({
  components: {
    TextField,
    Validation
  }
})
export default class RssConfigDialog extends Vue {
  validationErrors: { [key: string]: string[] } = {};
  url: string = "";
  deleteTargets: number[] = [];

  get sites() {
    return articleModule.displaySites
  }

  async submit() {
    this.$emit("submit");
    const site = await articleModule
      .submitNewSiteInfo(this.url)
      .catch(error => {
        const data = error.response.data;
        if (data.messages) {
          data.messages.forEach((msg: string) => {
            globalModule.pushErrorMessage(msg);
          });
        }
        this.url = "";
      });
    this.url = "";
    if (site instanceof SiteInfo) {
      globalModule.pushInfoMessage(`${site.site_name}を登録しました。`);
      articleModule.initArticles();
    }
  }

  async deleteSelectedSites() {
    const ids = this.sites
      .filter(site => site.isDeleteRequired)
      .map(site => site.id);
    this.$emit("submit");
    articleModule.deleteSiteInfo(ids);
    globalModule.pushInfoMessage("削除しました。");
  }
}
</script>
<style lang="stylus">
@require '../styles/palette.styl';

.rss-config-form {
  max-width: 350px;
  overflow: hidden;
}

.rss-config-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.rss-config-icon {
  cursor: pointer;
  font-size: 20px;
}

.rss-config-label {
  color: $primary;
  position: relative;

  &:after {
    position: absolute;
    content: '';
    background-color: $primary;
    height: 3px;
    width: 100%;
    border-radius: 2px;
    top: 100%;
    left: 0px;
  }
}

.rss-config-list {
  display: flex;
  flex-direction: column;
  text-align: left;

  &__item {
    margin-top: 5px;
  }
}
</style>
