<template>
  <div class="card" :class="classes" @click="$emit('click', $event)">
    <slot />
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
@require '../styles/palette.styl';

.card {
  padding: 0.5em 1em;
  font-size: 18px;
  text-align: left;
  user-select: none;

  &--clickable {
    // cursor: pointer;
    transition: background-color 0.2s;
    cursor: default;

    &:hover {
      background-color: rgba(0, 0, 0, 0.1);
    }
  }
}
</style>
