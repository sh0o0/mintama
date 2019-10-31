<template>
  <v-app :style="topStyle">
      <v-container>
        <v-layout class="align-center justify-center">
          <v-flex>
            <v-btn link href="/login-or-signup/" color="primary" width="300">login</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
  </v-app>
</template>

<script>
import { backgroundStyle, oauthBtns } from "@/mixins/top";
  export default {
    mixins: [backgroundStyle, oauthBtns]
  }
</script>
