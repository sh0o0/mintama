<template>
  <ul v-if="errors">
    <li v-for="(error, index) in errors" :key="formName + '-' + index">{{ error }}</li>
  </ul>
</template>

<script>
export default {
  props: {
    formName: String,
    errors: Array,
  },
};
</script>
<style scoped lang="sass">
ul
  font-size: 0.8rem
  list-style-type: none

  li
    color: #E53935


</style>