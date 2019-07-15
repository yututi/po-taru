<template>
  <div class="menu-holder">
    <slot name="activator" />
    <div class="menu-holder__menu menu" :class="{'menu--show':show}" :style="menuStyle">
      <slot name="menu" />
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Model, Watch, Vue } from "vue-property-decorator";
import { queryExact, getBindingClientRectSneaky } from "@/utlis";

@Component
export default class Menu extends Vue {
  @Prop({ type: String, default: "left", required: false })
  position!: string;
  @Prop({ type: Boolean, required: true })
  show!: boolean;
  menuStyle: { [key: string]: string } = {};
  calcStyles() {
    // なんか$elからとれないのでdocumentからとる
    // FIXME このコンポーネント2つ以上使うと破綻するのでidからとるように変更
    const holder = queryExact(document, ".menu-holder");
    const holderRect = holder.getBoundingClientRect();
    const menu = queryExact(document, ".menu") as HTMLElement;
    const menuRect = getBindingClientRectSneaky(menu);
    switch (this.position) {
      case "left":
      default:
        return {
          left: -menuRect.width + "px",
          top: holderRect.top + "px"
        };
    }
  }

  @Watch("show")
  onVisibilityChange(newVal: boolean, oldVal: boolean) {
    if (newVal) {
      this.menuStyle = this.calcStyles();
      setTimeout(() => {
        window.addEventListener(
          "click",
          () => {
            setTimeout(() => {
              this.$emit("update:show", false);
            }, 200);
          },
          { once: true }
        );
      }, 500);
    }
  }
}
</script>
<style lang="stylus">
@import '../styles/palette.styl';

.menu-holder {
  position: relative;

  &__menu {
    position: absolute;
  }
}

.menu {
  display: none;
  border: 1px solid gainsboro;
  opacity: 0;
  transition: opacity 0.3s;
  min-width: 120px;
  background-color: $bgColor;

  &--show {
    display: block;
    opacity: 1;
  }
}
</style>
