<template>
  <modal-dialog v-model="showDialog" :hideOnBgClick="false">
    <div class="form">
      <header class="form__header rss-config-header">
        <span>RSSフィード対象を登録します。</span>
        <i class="rss-config-icon fas fa-times-circle" @click="showDialog = false"></i>
      </header>
      <text-field class="form__field" label="サイト名" v-model="siteName"></text-field>
      <text-field class="form__field" label="URL" v-model="siteName"></text-field>
      <div class="form__action">
        <button class="button">登録</button>
      </div>
    </div>
  </modal-dialog>
</template>

<script lang="ts">
import { Component, Prop, Watch, Model, Vue } from "vue-property-decorator";
import ModalDialog from "@/components/ModalDialog.vue";
import TextField from "@/components/TextField.vue";

@Component({
  components: {
    ModalDialog,
    TextField
  }
})
export default class RssConfigDialog extends Vue {
  @Prop({ type: Boolean, default: false, required: false })
  value!: boolean;

  siteName: string = "";
  url: string = "";

  get showDialog(): boolean {
    return this.value;
  }

  set showDialog(isShow: boolean) {
    if (!isShow) {
      this.siteName = this.url = "";
    }
    this.$emit("input", isShow);
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
  font-size:20px;
}
</style>
