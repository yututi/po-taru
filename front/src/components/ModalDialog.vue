<template>
  <div class="modal" :class="{'modal--show':show}" @click="tryClose">
    <div class="modal__dialog dialog" @click.stop>
      <slot />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Model, Vue } from "vue-property-decorator";

@Component
export default class Dialog extends Vue {
  @Prop({ type: Boolean, default: false, required: false })
  value: boolean;

  @Prop({ type: Boolean, required: false, default: true })
  hideOnBgClick: boolean;

  get show() {
    return this.value;
  }
  set show(isShow: boolean) {
    this.$emit("input", isShow);
  }

  tryClose() {
    if (this.hideOnBgClick) {
      this.show = false;
    }
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
  transition: opacity 0.3s, visibility 0.3s;
  z-index: 998;

  &--show {
    visibility: visible;
    opacity: 1;

    .modal__dialog {
      transform: scale(1);
      border-radius: 5px;
    }
  }

  &__dialog {
    transform: scale(0);
    border-radius: 50%;
    transition: transform 0.5s, border-radius 0.5s;
  }
}

.dialog {
  background-color: $bgColor;
  overflow: hidden;
}
</style>
