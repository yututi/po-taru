<template>
  <div class="modal" :class="{'modal--show':show}" @click="show = false">
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
  value!: boolean;

  get show() {
    return this.value;
  }
  set show(isShow: boolean) {
    this.$emit("input", isShow);
  }

  showDialog() {
    this.show = false;
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
