<template>
  <div class="exp-panel" :class="{'is-open':isOpen}">
    <nav class="exp-panel__header exp-header" @click="togglePanel" v-rippuru>
      <a class="exp-header__icon">
        <i
          style="transition: transform 0.3s 0s ease;"
          :style="{transform:`rotate(${isOpen?90:0}deg)`}"
          class="fas fa-chevron-circle-right"
        ></i>
      </a>
      <a class="exp-header__title">{{title}}</a>
    </nav>
    <div class="exp-panel__body" :style="{'max-height':height+'px'}" :id="`exp-body-${id}`">
      <slot name="body"></slot>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
@Component({
  components: {}
})
export default class ExpansionPanel extends Vue {
  @Prop(String)
  id!: String;
  @Prop(String)
  title!: String;
  isOpen: boolean = false;
  height: number = 0;
  togglePanel() {
    this.isOpen = !this.isOpen;
    if (this.isOpen) {
      var el: HTMLElement | null = document.getElementById(
        `exp-body-${this.id}`
      );
      var height: number = el ? el.scrollHeight : 0;
      this.height = height;
    } else {
      this.height = 0;
    }
  }
  mounted() {}
}
</script>
<style lang="stylus">
@require '../styles/exp-panel.styl';
</style>