<template>
  <modal-dialog v-model="showDialog">
    <div class="form">
      <header>RSSフィード対象を登録します。</header>
      <input type="url" />
      <button></button>
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

  get showDialog(): boolean {
    return this.value;
  }

  set showDialog(isShow: boolean) {
    this.$emit("input", isShow);
  }
}
</script>
<style lang="stylus">
@require '../styles/palette.styl';

.modal {
  visibility: hidden;
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s;

  &--show {
    visibility: visible;
    opacity: 1;
  }

  &__dialog {
  }
}

.dialog {
  border: 1px solid gainsboro;
  background-color: $bgColor;
  padding: 0.5em;
}
</style>
