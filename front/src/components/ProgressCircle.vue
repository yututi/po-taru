<template>
  <svg class="progress" :class="classes" :viewBox="viewBox" xmlns="http://www.w3.org/2000/svg">
    <circle class="progress__circler" :style="circleStyle" :cx="center" :cy="center" :r="r" />
  </svg>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";

@Component
export default class ProgressCircle extends Vue {
  @Prop({ type: Boolean, required: false, default: true })
  value: boolean; // visibility

  @Prop({ type: Boolean, required: false, default: true })
  intermediate: boolean;

  @Prop({ type: Number, required: false, default: 6 })
  strokeWidth: number;

  get viewBox() {
    const size = this.r * 2 + this.strokeWidth;
    return `0 0 ${size} ${size}`;
  }

  get center() {
    return (this.r * 2 + this.strokeWidth) / 2;
  }

  get r() {
    return 50;
  }

  get visibility() {
    return this.value;
  }

  set visibility(value: boolean) {
    this.$emit("input", value);
  }

  get circleStyle() {
    return {
      "stroke-width": this.strokeWidth
    };
  }

  get classes() {
    return {
      "progress--intermediate": this.intermediate
    };
  }
}
</script>
<style lang="stylus">
@require '../styles/palette.styl';

$rotateTime = 1.5s;

.progress {
  opacity: 0;

  &--intermediate {
    visibility: visible;
    opacity: 1;
    animation: rotate $rotateTime infinite;
  }

  &--intermediate &__circler {
    stroke: blue;
    fill: transparent;
    animation: dynamic-circumference $rotateTime infinite;
  }
}

@keyframes dynamic-circumference {
  0% {
    stroke-dasharray: 0 315;
    stroke-dashoffset: 0;
  }

  50% {
    stroke-dasharray: 315 315;
    stroke-dashoffset: 0;
  }

  99.9%, to {
    stroke-dasharray: 315 315;
    stroke-dashoffset: -315;
  }
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }

  99.9%, to {
    transform: rotate(360deg);
  }
}
</style>
