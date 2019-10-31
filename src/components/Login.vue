<template>
  <v-card class="form">
    <v-toolbar color="primary" dark flat>
      <v-row align="center">
        <v-col>
          <v-toolbar-title class="font-weight-bold display-1">Login</v-toolbar-title>
        </v-col>
        <v-col cols="6" class="text-right">
          <v-btn
            v-for="oauth in oauthBtns"
            :key="oauth.name"
            :href="oauth.href"
            :class="'ma-2 ' + oauth.class"
            small
            rounded
            light
            color="normal"
          >{{ oauth.name }}</v-btn>
        </v-col>
      </v-row>
    </v-toolbar>
    <v-card-text>
      <v-form>
        <div v-for="form in formObj" :key="form.name" class="form-item">
          <FormError :name="form.name" :errors="form.errors"></FormError>
          <v-text-field
            v-if="form.name !== 'non_field_errors'"
            v-model="form.value"
            :type="form.type"
            :name="form.name"
            :autofocus="form.autofocus"
            :required="form.required"
            :label="form.label"
            :prepend-icon="form.prependIcon"
            :id="form.id"
          ></v-text-field>
        </div>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="login()" id="login">ログイン</v-btn>
      <v-btn outlined color="teal" @click="toggleLoginOrSignup" id="move-signup">新規登録</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapMutations } from "vuex";
import { Api } from "@/asynchronous/api";
import FormError from "@/components/FormError";
import FormHelper from '@/helper/form'
import { oauthBtns } from "@/mixins/top";

export default {
  mixins: [oauthBtns],
  props: {
    csrftoken: String,
  },
  data() {
    return {
      formObj: {
        username: {
          name: "username",
          value: "",
          errors: [],
          type: "text",
          autofocus: true,
          required: true,
          label: "Username",
          prependIcon: "person",
          id: 'username',
        },
        password: {
          name: "password",
          value: "",
          errors: [],
          type: "password",
          autofocus: false,
          required: true,
          label: "Password",
          prependIcon: "lock",
          id: 'password'
        },
        non_field_errors: {
          name: "non_field_errors",
          value: "",
          errors: [],
          type: "hidden",
          autofocus: false,
          required: false,
          label: "",
          prependIcon: "",
        }
      },
    };
  },
  components: {
    FormError
  },
  methods: {
    login() {
      const that = this;
      Api.post('login', this.formObj, this.csrftoken)
      .then(response => {
        let redirectPath = '/';
        // hrefが#以降を受け付けないため実装不可。history modeにする必要あり。
        // const query = location.href.split('?').slice(-1)
        // const hash = location.search.slice(1).split('&')
        // for (const i in hash) {
        //   const keyValue = hash[i].split('=');
        //   if (keyValue[0] === 'next') {
        //     redirectPath = keyValue[1];
        //     break;
        //   }
        // }
        location.href = redirectPath;
      }).catch(err => {
        FormHelper.assignErrors(that.formObj, err.response.data);
      })
    },
    toggleLoginOrSignup() {
      this.$emit("toggleLoginOrSignup");
    }
  }
};
</script>
<style scoped lang="sass">
.form
  width: 500px

@media screen and (max-device-width: 480px)
    .form
      width: 700px
    .form-item
      margin: 30px auto
</style>