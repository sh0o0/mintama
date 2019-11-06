<template>
  <v-card class="form">
    <v-toolbar color="teal" dark flat>
      <v-row align="center">
        <v-col>
          <v-toolbar-title class="font-weight-bold display-1">Signup</v-toolbar-title>
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
            :id="formData.id"
          ></v-text-field>
        </div>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="teal" @click="signup()" id="signup">登録</v-btn>
      <v-btn outlined color="primary" @click="toggleLoginOrSignup" id="move-login">ログイン</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapMutations } from "vuex";
import { debouncedCheckOneForm, Api } from "@/asynchronous/api";
import FormError from "@/components/FormError";
import FormHelper from "@/helper/form";
import { oauthBtns } from "@/mixins/top";

export default {
  mixins: [oauthBtns],
  props: {
    csrftoken: String
  },
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
          prependIcon: "person",
          id: 'username',
        },
        // email: {
        //   name: "email",
        //   value: "",
        //   errors: [],
        //   type: "email",
        //   autofocus: false,
        //   required: true,
        //   label: "Email",
        //   prependIcon: "email",
        //   id: 'email',
        // },
        password1: {
          name: "password1",
          value: "",
          errors: [],
          type: "password",
          autofocus: false,
          required: true,
          label: "Password",
          prependIcon: "lock",
          id: 'password1',
        },
        password2: {
          name: "password2",
          value: "",
          errors: [],
          type: "password",
          autofocus: false,
          required: true,
          label: "Confirm Password",
          prependIcon: "lock",
          id: 'password2',
        },
        non_field_errors: {
          name: "non_field_errors",
          value: "",
          errors: [],
          type: "hidden",
          autofocus: false,
          required: false,
          label: "",
          prependIcon: ""
        }
      }
    };
  },
  components: {
    FormError
  },
  methods: {
    signup() {
      const that = this;
      Api.post("signup", this.formObj, this.csrftoken, false).then(function(response) {
        location.href = "/";
      }).catch(err => {
        FormHelper.assignErrors(that.formObj, err.response.data);
      });
    },
    toggleLoginOrSignup() {
      this.$emit("toggleLoginOrSignup");
    }
  },
  watch: {
    "formObj.username.value": function() {
      debouncedCheckOneForm("signup", "username", this.formObj);
    },
    "formObj.password1.value": function() {
      debouncedCheckOneForm("signup", "password1", this.formObj);
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