<template>
  <div class="modal" :class="classes" @click="$emit('click', $event)">
    <div class="modal__dialog dialog">
      <slot />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";

@Component
export default class Card extends Vue {
  @Prop({ type: Boolean, required: false, default: false })
  clickable!: boolean;

  get classes() {
    return {
      "card--clickable": this.clickable
    };
  }
}
</script>
<style lang="stylus">
// @require '../styles/palette.styl';
.modal {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;

  &__dialog {
      
  }
}
</style>
