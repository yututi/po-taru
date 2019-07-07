<template>
  <layout>
    <template v-slot:content>
      <div class="home">
        <img alt="Vue logo" src="../assets/logo.png" />
        <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
      </div>
    </template>
  </layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Layout from "@/views/Layout.vue";

@Component({
  components: {
    Layout
  }
})
export default class Home extends Vue {}
</script>
