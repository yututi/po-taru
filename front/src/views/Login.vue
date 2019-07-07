<template>
  <div class="login">
    <div class="login-form">
      <div class="login-form__field field">
        <label for="id">ID</label>
        <input id="id" type="text" v-model="id" />
      </div>
      <div class="login-form__field field password-field">
        <label for="password">Password</label>
        <input id="password" :type="isPwdHiding?'password':'text'" v-model="pwd" />
        <div class="password-field__eye" @click="togglePwdVisibility">
          <i v-if="isPwdHiding" class="far fa-eye"></i>
          <i v-else class="far fa-eye-slash"></i>
        </div>
      </div>
      <div class="login-form__action">
        <button @click="login" class="button">Login</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { authModule } from "@/stores";

@Component
export default class Login extends Vue {
  isPwdHiding: boolean = true;
  id: string = "";
  pwd: string = "";

  togglePwdVisibility() {
    this.isPwdHiding = !this.isPwdHiding;
  }

  async login() {
    const isAuhenticated = await authModule.login(this.id, this.pwd);
    if (!isAuhenticated) {
      return;
    }
    if (
      this.$route.query.redirect &&
      typeof this.$route.query.redirect === "string"
    ) {
      this.$router.push(this.$route.query.redirect);
    } else {
      this.$router.push("/");
    }
  }
}
</script>
<style lang="stylus">
.login {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.login-form {
  max-width: 400px;
  margin: auto;
  display: flex;
  flex-direction: column;
  padding: 1em;
  border: solid 1px gainsboro;
  border-radius: 5px;

  &__field + &__field {
    margin-top: 1em;
  }

  &__action {
    margin-top: 1em;
    display: flex;
    justify-content: flex-end;

    & > button {
      font-size: 16px;
      font-weight: 100;
    }
  }
}

.field {
  display: flex;
  align-items: baseline;

  & > label {
    padding: 0.3em;
    text-align: right;
    color: gray;
    font-size: 16px;
    font-weight: 100;
    flex: 1;
  }

  & > input {
    padding: 0.3em;
    border: solid 1px gainsboro;
    border-radius: 0.2em;
    flex: 2;
  }
}

.password-field {
  position: relative;

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
