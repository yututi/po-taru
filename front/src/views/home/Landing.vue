<template>
  <div class="landing">
    <h1 class="landing__ymd">
      {{year}}
      <small>年</small>
      {{month}}
      <small>月</small>
      {{date}}
      <small>日</small>
    </h1>
    <h1 class="landing__time">
      {{hours}}
      <small>時</small>
      {{minutes}}
      <small>分</small>
      {{seconds}}
      <small>秒</small>
    </h1>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import IconMenu from "@/components/IconMenu.vue";

@Component({
  components: {
    IconMenu
  }
})
export default class Landing extends Vue {
  datetime: Date = new Date();
  _cancelId!: number;
  get year() {
    return this.datetime.getFullYear();
  }
  get month() {
    return this.datetime.getMonth() + 1;
  }
  get date() {
    return this.datetime.getDate();
  }
  get hours() {
    return this.pad(this.datetime.getHours());
  }
  get minutes() {
    return this.pad(this.datetime.getMinutes());
  }
  get seconds() {
    return this.pad(this.datetime.getSeconds());
  }
  pad(num: number) {
    return num.toString().padStart(2, "0");
  }
  mounted() {
    this._cancelId = setInterval(() => {
      this.datetime = new Date();
    }, 1000);
  }
  beforeDestroy() {
    clearInterval(this._cancelId);
  }
}
</script>
<style lang="stylus">
.landing {
  text-align: center;
  overflow: hidden;

  &__ymd {
    font-weight: 100;
  }

  &__time {
    font-weight: 100;
    font-size: 3em;
  }
}
</style>
