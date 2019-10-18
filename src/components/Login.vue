<template>
  <v-card class="elevation-12">
    <v-toolbar color="primary" dark flat>
      <v-row align="center">
        <v-col cols="12" md="3">
          <v-toolbar-title>Login</v-toolbar-title>
        </v-col>
        <v-col cols="12" md="9">
          <v-btn
            v-for="oauth in oauthBtns"
            :key="oauth.name"
            :href="oauth.href"
            small
            rounded
            light
            color="normal"
            class="ma-2"
          >{{ oauth.name }}</v-btn>
        </v-col>
      </v-row>
    </v-toolbar>
    <v-card-text>
      <v-form name="login" method="post">
        <div v-for="form in formObj" :key="form.name">
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
          ></v-text-field>
        </div>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="submit()">ログイン</v-btn>
      <v-btn outlined color="teal" @click="toggleLoginOrSignup">新規登録</v-btn>
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
          prependIcon: "person"
        },
        password: {
          name: "password",
          value: "",
          errors: [],
          type: "password",
          autofocus: false,
          required: true,
          label: "Password",
          prependIcon: "lock"
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
    submit() {
      const that = this;
      Api.post('login', this.formObj, this.csrftoken)
      .then(function(response) {
        if (FormHelper.isEmpty(response.data)) {
          location.href = '/';
        } else {
          FormHelper.assignErrors(that.formObj, response.data);
        }
      })
    },
    toggleLoginOrSignup() {
      this.$emit("toggleLoginOrSignup");
    }
  }
};
</script>