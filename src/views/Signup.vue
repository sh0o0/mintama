<template>
  <v-app :style="topStyle">
    <v-content>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="teal"
                dark
                flat
              >
                <v-toolbar-title>Signup</v-toolbar-title>
                <v-spacer></v-spacer>
                <v-layout wrap>
                  <v-flex xs12 sm6 md4 text-center my-5>
                    <v-btn href="/socials/login/twitter" small rounded light color="normal">twitter</v-btn>
                  </v-flex>
                  <v-flex xs12 sm6 md4 text-center my-5>
                    <v-btn href="/socials/login/google-oauth2/" small rounded light color="normal">google</v-btn>
                  </v-flex>
                  <v-flex xs12 sm6 md4 text-center my-5>
                    <v-btn href="/socials/login/github/" small rounded light color="normal">github</v-btn>
                  </v-flex>
                </v-layout>
              </v-toolbar>
              <v-card-text>
                <v-form name="signup" method="post">
                  <input type="hidden" name="csrfmiddlewaretoken" :value="csrftoken">
                  <FormError name="username" :errors="usernameErrors"></FormError>
                  <v-text-field
                    type="text"
                    name="username"
                    autofocus="autofocus"
                    required="required"
                    id="id_username"
                    v-model="usernameValue"
                    
                    label="Username"
                    prepend-icon="person"
                  ></v-text-field>

                  <FormError formName="email" :errors="emailErrors" class="mt-3"></FormError>
                  <v-text-field
                    type="email"
                    name="email"
                    required="required"
                    id="id_email"
                    v-model="emailValue"
                    
                    label="Email"
                    prepend-icon="email"
                  ></v-text-field>

                  <FormError formName="password1" :errors="password1Errors" class="mt-3"></FormError>
                  <v-text-field
                    type="password"
                    name="password1"
                    required="required"
                    id="id_password1"
                    v-model="password1Value"
                    
                    label="Password"
                    prepend-icon="lock"
                  ></v-text-field>

                  <FormError formName="password2" :errors="password2Errors" class="mt-3"></FormError>
                  <v-text-field
                    type="password"
                    name="password2"
                    required="required"
                    id="id_password2"
                    
                    label="Confirm Password"
                    prepend-icon="lock"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <FormError name='non_field_error' :errors="non_field_errors"></FormError>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="teal" @click="submit()">登録</v-btn>
                <v-btn outlined color="primary" href="/login/">ログイン</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  //normal modules
  import _ from 'lodash'
  import Cookies from 'js-cookie'
  //vue modules
  import Vue from 'vue'
  import FormError from '@/components/FormError'
  //mixins
  import { topStyle } from '@/top_style'

  export default {
    mixins: [topStyle],
    props: [
      'csrftoken', 

      'username_value',
      'email_value',

      'username_errors', 
      'email_errors',
      'password1_errors', 
      'password2_errors', 
      'non_field_errors',
    ],
    data() {
        return {
            usernameValue: this.username_value,
            emailValue: this.email_value,
            password1Value: this.password1_value,
            usernameErrors: this.username_errors,
            emailErrors: this.email_errors,
            password1Errors: this.password1_errors,
            password2Errors: this.password2_errors,
        }
    },
    components: {
      FormError,
    },
    created: function() {
      this.debouncedCheckOneForm = _.debounce(this.checkOneForm, 1000)
    },
    methods: {
      //コードの汎用化を試みるも断念（理由下記）
      //lodashはreturnできない・thisを渡せない
      checkOneForm: function(formName) {
        //#を取り除く（2手法あり）
        // const href = location.href.slice(0, -2);
        const sliceIndex = location.href.indexOf('#/');
        const href = location.href.slice(0, sliceIndex);

        const url = `${href}check_${formName}/`; 
        const data = {[formName]: this[formName + 'Value']};
        const csrftoken = Cookies.get('csrftoken');
        const headers = {'X-CSRFToken': csrftoken};
        const that = this;

        Vue.axios.post(url, data, {headers: headers})
        .then(function(response) {
            if (response.data['available'] === true) {
                that[formName + 'Errors'] = [];
            } else {
                that[formName + 'Errors'] = response.data['errors'];
            }
        })
        .catch(function(error) {
            throw new Error(`Api ${error}`);
        })
      },
      submit: () => {
        const form = document.forms['signup']
        form.submit()
      }
    },
    watch: {
      usernameValue: function() {
        this.debouncedCheckOneForm('username');
      },
      password1Value: function() {
        this.debouncedCheckOneForm('password1');
      },
    },
  }
</script>