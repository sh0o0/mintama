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
                color="primary"
                dark
                flat
              >
                <v-toolbar-title>Login</v-toolbar-title>
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
                <FormError name="username" :errors="username_errors"></FormError>
                <v-form name="login" method="post">
                  <input type="hidden" name="csrfmiddlewaretoken" :value="csrftoken">
                  <v-text-field
                    type="text"
                    name="username"
                    autofocus="autofocus"
                    required="required"
                    id="id_username"
                    :value="username_value"
                    
                    label="Username"
                    prepend-icon="person"
                  ></v-text-field>

                  <FormError name="password" :errors="password_errors"></FormError>
                  <v-text-field
                    type="password"
                    name="password"
                    required="required"
                    id="id_password"
                    
                    label="Password"
                    prepend-icon="lock"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <FormError name='non_field_error' :errors="non_field_errors"></FormError>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="submit()">ログイン</v-btn>
                <v-btn outlined color="teal" href="/signup/">新規登録</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
  import FormError from '@/components/FormError'
  import { topStyle } from '@/top_style'

  export default {
    mixins: [topStyle],
    props: [
      'csrftoken', 
      'username_value',
      'username_errors', 
      'password_errors', 
      'non_field_errors',
    ],
    components: {
      FormError,
    },
    methods: {
      submit: () => {
        const form = document.forms['login']
        form.submit()
      }
    },
  }
</script>