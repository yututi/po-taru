<template>
  <div class="login">
    <validation :messages.sync="validationErrors.messages">
      <div class="login-form form">
        <validation :messages.sync="validationErrors.username" class="form__field">
          <text-field :value.sync="id" label="Id" />
        </validation>
        <validation :messages.sync="validationErrors.password" class="form__field">
          <text-field password :value.sync="pwd" label="Password" />
        </validation>
        <div class="form__action">
          <button @click="login" v-ripple class="button">Login</button>
        </div>
      </div>
    </validation>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TextField from "@/components/TextField.vue";
import Validation from "@/components/Validation.vue";
import { authModule } from "@/stores/auth";
import { AxiosResponse, AxiosError } from "axios";

@Component({
  components: {
    TextField,
    Validation
  }
})
export default class Login extends Vue {
  isPwdHiding: boolean = true;
  id: string = "";
  pwd: string = "";
  validationErrors: { [key: string]: string[] } = {};

  async login() {
    await authModule
      .login({ id: this.id, password: this.pwd })
      .catch(this.onAuthError);

    if (!authModule.isAuthenticated) {
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
  onAuthError(error: AxiosError) {
    this.pwd = "";
    if (error.response) {
      const errMsgs = error.response.data || {};
      this.validationErrors = errMsgs;
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
  border: solid 1px gainsboro;
  border-radius: 5px;
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
