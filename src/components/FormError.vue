<template>
  <ul v-if="errors">
    <li v-for="(error, index) in errorsArray" :key="formName + '-' + index">{{ error }}</li>
  </ul>
</template>

<script>
export default {
  props: {
    formName: String,
    errors: [String, Array]
  },
  computed: {
    errorsArray: function() {
      if (typeof this.errors == "string") {
        return this.errors.split(",");
      }
      return this.errors;
    }
  }
};
</script>
<style scoped lang="sass">
ul
  font-size: 0.8rem
  list-style-type: none

  li
    color: #E53935


</style>