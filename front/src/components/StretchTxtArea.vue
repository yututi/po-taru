<template>
  <div
    class="text-area"
    :class="classes"
    spellcheck="false"
    v-text="text"
    :contenteditable="editable"
    @input="onInput"
  ></div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";

@Component
export default class ProgressCircle extends Vue {
  @Prop({ type: String, required: false, default: "" })
  value: string; // text

  @Prop({ type: Boolean, default: true })
  editable: boolean;

  text: string = "";

  get classes() {
    return {
      "text-area--disable": !this.editable
    };
  }

  @Watch("value")
  valueChanged(newValue: string) {
    console.log(document.activeElement);
    if (document.activeElement != this.$el) {
      console.log("set", newValue);
      this.$el.innerHTML = newValue;
    }
  }

  onInput(e: any) {
    this.$emit("input", e.target.innerText);
  }

  mounted() {
    this.text = this.value;
  }
}
</script>
<style lang="stylus">
@require '../styles/palette.styl';

.text-area {
  white-space: pre-wrap;
  box-sizing: border-box;
  border-radius: 10px;
  outline: none;
  border: 1px solid gainsboro;
  background-color: #fff8f8;
  text-align: left;
  line-height: 1.5em;

  &:focus {
    border: 2px solid $accent;
    padding: 11px;
  }

  &--disable {
    background-color: #f8f8f8;
  }
}
</style>
