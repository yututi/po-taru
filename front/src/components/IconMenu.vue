<!-- FIXME 試行錯誤したせいでクラス名が滅茶苦茶 -->
<template>
  <!-- 基点 -->
  <div class="im-wrapper" @click.stop :class="classes">
    <!-- 枠 -->
    <div class="im-menu">
      <!-- コンテンツの入れ物 -->
      <div class="im-menu__content" :class="contentClasses" :style="contentStyles">
        <!-- スライドイン用 -->
        <div class="content-slide im-content" :class="slideClasses">
          <!-- コンテンツヘッダ -->
          <div class="im-content__header">
            <div class="im-close-icon" @click="hideMenu">
              <fa-icon icon="times-circle" />
            </div>
          </div>
          <!-- コンテンツ -->
          <div class="im-content__body">
            <slot />
          </div>
        </div>
      </div>
      <!-- メニュー表示用アイコン -->
      <div class="im-menu__icon" @click.stop="showMenu">
        <fa-icon icon="cog" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";

@Component
export default class Card extends Vue {
  isShown: boolean = false;

  @Prop({ type: String, required: false, default: "top-left" })
  position: string;

  @Prop({ type: Boolean, required: false, default: false })
  hideOnOtherClick: boolean;

  height: number = 50;
  width: number = 50;

  _window: Window;
  _listenr: EventListener;

  get classes() {
    return {
      "im-wrapper--open": this.isShown
    };
  }

  get contentClasses() {
    const classes: { [key: string]: boolean } = {};
    classes[`im-menu__content--${this.position}`] = true;
    return classes;
  }

  get slideClasses() {
    const classes: { [key: string]: boolean } = {};
    classes[`content-slide--${this.position}`] = true;
    return classes;
  }

  get contentStyles() {
    return {
      height: `${this.height}px`,
      width: `${this.width}px`
    };
  }

  showMenu() {
    this.isShown = true;
    // const el: HTMLElement = document.getElementById(`test`);
    const el: HTMLElement = this.$el.querySelector(".im-content");
    this.height = el.scrollHeight;
    this.width = el.scrollWidth;

    if (this.hideOnOtherClick) {
      this._listenr = () => {
        this.hideMenu();
        this._window.removeEventListener("click", this._listenr);
        this._listenr = null;
      };
      this._window.addEventListener("click", this._listenr);
    }
  }
  hideMenu() {
    this.isShown = false;
    this.height = 50;
    this.width = 50;
  }
  mounted() {
    this._window = window;
  }
}
</script>
<style lang="stylus">
@require '../styles/palette.styl';

.im-wrapper {
  position: relative;
  height: 50px;
  width: 50px;
  z-index: 5;

  &--open {
    .im-menu {
      border-color: transparent;

      &__icon {
        transform: rotate(359deg);
        opacity: 0;
        visibility: hidden;
      }

      &__content {
        border-radius: 5px;
        border: 1px solid gainsboro;
        visibility: visible;
        cursor: default;
      }
    }

    .content-slide {
      visibility: visible;
      transform: translateX(0%);
    }

    .im-close-icon {
      display: none;
    }
  }
}

.im-menu {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;

  &__icon {
    transition: all 0.3s;
    opacity: 1;
    font-size: 20px;
    color: $primary;
    z-index: 2;
    height: 50px;
    width: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }

  &__content {
    box-sizing: border-box;
    position: absolute;
    transition: all 0.3s;
    border-radius: 50%;
    border: 1px solid gainsboro;
    cursor: pointer;
    overflow: hidden;
    background-color: $bgColor;

    &--top-left {
      right: 0px;
      bottom: 0px;
    }

    &--bottom-left {
      right: 0px;
      top: 0px;
    }
  }
}

.content-slide {
  position: absolute;
  overflow: hidden;
  transform: translateX(-100%);
  transition: all 0.3s;
  visibility: hidden;

  &--top-left {
    bottom: 0px;
  }

  &--bottom-left {
    top: 0px;
  }
}

.im-content {
  display: flex;
  flex-direction: column;

  &__header {
    display: flex;
    justify-content: flex-end;

    .im-close-icon {
      font-size: 20px;
      color: $accent;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 50px;
      width: 50px;
      cursor: pointer;
    }
  }

  &__body {
    // padding: 0 10px 10px 10px;
  }
}
</style>
