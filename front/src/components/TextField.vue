<template>
  <div class="field">
    <label class="field__label" :for="label">{{label}}</label>
    <input
      class="field__input"
      :id="label"
      :type="inputType"
      v-model="text"
    />
    <div v-if="isPassword" class="field__eye" @click="isPasswordHiding = !isPasswordHiding">
      <i v-if="isPasswordHiding" class="far fa-eye"></i>
      <i v-else class="far fa-eye-slash"></i>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import InputForm from "@/components/InputForm.vue";

@Component
export default class TextField extends Vue {
  @Prop({ required: true, type: String }) value?: string;
  @Prop({ required: true, type: String }) label?: string;
  @Prop({ required: false, type: String, default: "text" }) type?: string;
  isPasswordHiding: boolean = true;
  get inputType() {
    return this.isPassword && !this.isPasswordHiding ? 'text' : this.type;
  }
  get isPassword(){
      return this.type == 'password'
  }
  get text() {
    return this.value;
  }
  set text(value: string) {
    this.$emit("input", value);
  }
}
</script>
<style lang="stylus">
.field {
  display: flex;
  align-items: center;
  position: relative;

  &__label {
    padding: 0.3em;
    text-align: right;
    color: gray;
    font-size: 16px;
    font-weight: 100;
    flex: 1;
    white-space: nowrap;
  }

  &__input {
    padding: 0.3em;
    border: solid 1px gainsboro;
    border-radius: 0.2em;
    flex: 2;
  }

  &__validation-error {
    position: absolute;
    left: 100%;
    top: 0px;
    height: 100%;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s;

    &--show {
      visibility: visible;
      opacity: 1;
    }
  }

  &__eye {
    position: absolute;
    padding: 0 0.3em;
    top: 0;
    right: 0;
    height: 100%;
    font-size: 20px;
    color: lightgray;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
}
</style>
