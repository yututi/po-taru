<template>
  <div class="landing">
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import IconMenu from "@/components/IconMenu.vue";

@Component({
})
export default class Landing extends Vue {
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
