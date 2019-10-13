<template>
  <v-card class="elevation-12">
    <v-toolbar color="teal" dark flat>
      <v-toolbar-title>Signup</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-layout wrap>
        <v-flex v-for="oauth in oauthBtns" :key="oauth.name" xs12 sm6 md4 text-center my-5>
          <v-btn :href="oauth.href" small rounded light color="normal">{{ oauth.name }}</v-btn>
        </v-flex>
      </v-layout>
    </v-toolbar>
    <v-card-text>
      <v-form name="signup" method="post">
        <div v-for="formData in formObj" :key="formData.name">
          <FormError :name="formData.name" :errors="formData.errors"></FormError>
          <v-text-field
            v-if="formData.name !== 'non_field_errors'"
            v-model="formData.value"
            :type="formData.type"
            :name="formData.name"
            :autofocus="formData.autofocus"
            :required="formData.required"
            :label="formData.label"
            :prepend-icon="formData.prependIcon"
          ></v-text-field>
        </div>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="teal" @click="submit()">登録</v-btn>
      <v-btn outlined color="primary" @click="toggleLoginOrSignup">ログイン</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapMutations } from "vuex";
import { debouncedCheckOneForm, Api } from "@/asynchronous/api";
import FormError from "@/components/FormError";
import FormHelper from '@/helper/form'
import { oauthBtns } from "@/mixins/top";

export default {
  mixins: [oauthBtns],
  data() {
    return {
      sample: {},
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
        email: {
          name: "email",
          value: "",
          errors: [],
          type: "email",
          autofocus: false,
          required: true,
          label: "Email",
          prependIcon: "email"
        },
        password1: {
          name: "password1",
          value: "",
          errors: [],
          type: "password",
          autofocus: false,
          required: true,
          label: "Password",
          prependIcon: "lock"
        },
        password2: {
          name: "password2",
          value: "",
          errors: [],
          type: "password",
          autofocus: false,
          required: true,
          label: "Confirm Password",
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
      Api.post('signup', this.formObj)
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
    },
  },
  watch: {
    "formObj.username.value": function() {
      debouncedCheckOneForm('signup', 'username', this.formObj);
    },
    "formObj.password1.value": function() {
      debouncedCheckOneForm('signup', 'password1', this.formObj);
    }
  },
};
</script>