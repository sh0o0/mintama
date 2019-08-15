<template>
  <button type="button" @click="goTo">押さないでください！</button>
</template>

<script>
  export default {
    props:{
      pathname: {
        type: String,
        required: true
      }
    },
    methods: {
      goTo() {
        this.$router.push({name: this.pathname})
      }
    }
  }
</script>

<style scoped lang="sass">
  button
    width: 80%
    background-color: transparent
    color: #000000
    border: 2px solid #000000
    border-radius: 5px
    min-height: 50px
    text-transform: uppercase
    &:hover
        background-color: #ffefd5
        color: #000000
        border-color: #000000
</style>