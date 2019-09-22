<template>
  <v-app>
    <h2 class="heading">アカウント</h2>
    <Profile></Profile>
  </v-app>
</template>
<script>
import Profile from "@/components/Profile";

export default {
  data() {
    return {};
  },
  components: {
    Profile
  }
};
</script>