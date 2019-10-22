<template>
  <v-app :style="topStyle">
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
            <transition name="fade" mode="out-in">
              <component :is="LoginOrSignup" :csrftoken="csrftoken" @toggleLoginOrSignup="toggleLoginOrSignup()"></component>
            </transition>
        </v-row>
      </v-container>
    </v-content>
  </v-app>
</template>
<script>
import { mapGetters } from "vuex";
import Login from "@/components/Login";
import Signup from "@/components/Signup";
import { backgroundStyle } from "@/mixins/top";

export default {
  mixins: [backgroundStyle],
  props: {
    csrftoken: String,
  },
  data() {
    return {
      LoginOrSignup: "Login"
    };
  },
  components: {
    Login,
    Signup
  },
  methods: {
    toggleLoginOrSignup() {
      if (this.LoginOrSignup === "Login") {
        this.LoginOrSignup = "Signup";
      } else {
        this.LoginOrSignup = "Login";
      }
    }
  }
};
</script>
<style scoped lang="sass">
.fade-enter-active, .fade-leave-active 
  transition: opacity .2s ease

.fade-enter, .fade-leave-to 
  opacity: 0
</style>