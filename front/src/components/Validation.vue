<template>
  <div class="validation" @keydown.passive="$emit('update:messages',[])">
    <slot />
    <div class="validation__box" :class="{'validation__box--show':hasMessage}">{{displayMessages}}</div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class Validation extends Vue {
  @Prop({ required: false, type: Array }) messages?: Array<string>;
  get hasMessage() {
    return this.messages && this.messages.length > 0;
  }
  get displayMessages() {
    return this.messages ? this.messages.join(", ") : "";
  }
}
</script>
<style lang="stylus">
$validationErrorColor = orange;
$validationErrorTxtColor = white;

.validation {
  position: relative;

  &__box {
    position: absolute;
    left: calc(100% + 0.5em);
    top: 0px;
    height: 100%;
    max-width: 0px;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s;
    display: flex;
    align-items: center;
    border-radius: 5px;
    color: $validationErrorTxtColor;
    background-color: $validationErrorColor;
    box-shadow: 0 0 4px 2px gainsboro;

    &--show {
      visibility: visible;
      opacity: 1;
      z-index: 20;
      width: fit-content;
      max-width: 300px;
      padding: 0 0.3em;

      &::before {
        content: '';
        position: absolute;
        left: -12px;
        width: 0px;
        height: 0px;
        margin: auto;
        border-style: solid;
        border-color: transparent $validationErrorColor transparent transparent;
        border-width: 6px;
      }
    }
  }
}
</style>
