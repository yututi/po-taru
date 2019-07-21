<template>
  <modal-dialog v-model="showDialog" :hideOnBgClick="false">
    <div class="form">
      <header class="form__header rss-config-header">
        <span>RSSフィード設定</span>
        <i class="rss-config-icon fas fa-times-circle" @click="showDialog = false"></i>
      </header>
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
      <validation class="form__field" :messages.sync="validationErrors.url">
        <text-field type="url" label="URL" v-model="url"></text-field>
      </validation>
      <div class="form__action">
        <button class="button" @click="submit">登録</button>
      </div>
    </div>
  </modal-dialog>
</template>

<script lang="ts">
import { Component, Prop, Watch, Model, Vue } from "vue-property-decorator";
import ModalDialog from "@/components/ModalDialog.vue";
import TextField from "@/components/TextField.vue";
import Validation from "@/components/Validation.vue";
import { articleModule } from "@/stores/article";
import { authModule } from "../stores/auth";
import { SiteInfo } from "@/dto";

class CheckableRssInfo {
  constructor(public site: SiteInfo, public isChecked: boolean) {}
}

@Component({
  components: {
    ModalDialog,
    TextField,
    Validation
  }
})
export default class RssConfigDialog extends Vue {
  @Prop({ type: Boolean, default: false, required: false })
  value!: boolean;

  validationErrors: { [key: string]: string[] } = {};
  url: string = "";
  deleteTargets: number[] = [];

  get showDialog(): boolean {
    return this.value;
  }

  set showDialog(isShow: boolean) {
    if (!isShow) {
      this.url = "";
    }
    this.$emit("input", isShow);
  }

  get sites() {
    return Object.values(articleModule.displaySites);
  }

  async submit() {
    await articleModule.submitNewSiteInfo(this.url).catch(error => {
      const data = error.response.data;
      this.validationErrors = data;
      data.messages && alert(data.messages.join(", "));
    });
  }

  async deleteSelectedSites() {
    const ids = this.sites.filter(site => site.isDeleteRequired).map(site => site.id);
    articleModule.deleteSiteInfo(ids)
  }
}
</script>
<style lang="stylus">
@require '../styles/palette.styl';

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
