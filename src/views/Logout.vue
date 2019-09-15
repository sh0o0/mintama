<template>
  <v-app :style="topStyle">
      <v-container>
        <v-layout class="align-center justify-center">
          <v-flex>
            <v-btn link href="/login/" color="primary">login</v-btn>
            <v-btn link href="/signup/" color="teal">Singup</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
  </v-app>
</template>

<script>
import { topStyle } from '@/top_style'
  export default {
    mixins: [topStyle]
  }
</script>
