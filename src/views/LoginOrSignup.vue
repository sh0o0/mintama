<template>
  <transition name="fade" mode="out-in">
    <component :is="getLoginOrSignup"></component>
  </transition>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
  components: {
    Login,
    Signup
  },
  computed: {
    ...mapGetters('user', ['getLoginOrSignup']),
  }
};
</script>
<style scoped lang="sass">
.fade-enter-active, .fade-leave-active 
  transtion: opacity .3s ease

.fade-enter, .fade-leave-to 
  opacity: 0
</style>