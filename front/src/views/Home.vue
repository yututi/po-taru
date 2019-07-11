<template>
  <layout>
    <template v-slot:content>
      <div class="home">
        <img alt="Vue logo" src="../assets/logo.png" />
        <button @click="doSomething">do something</button>
      </div>
    </template>
  </layout>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Layout from "@/views/Layout.vue";
import axios from "axios";

@Component({
  components: {
    Layout
  }
})
export default class Home extends Vue {
  async doSomething() {
    const response = await axios.post("dosomething");
    alert(response.data.message);
  }
}
</script>
