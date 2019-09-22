<template>
  <v-menu
    v-model="toggleMenu"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    full-width
    max-width="290px"
    min-width="290px"
  >
    <template v-slot:activator="{ on }">
      <v-text-field
        v-model="dateFormatted"
        :label="form.label"
        :prepend-icon="form.prependIcon"
        v-on="on"
        readonly
      ></v-text-field>
    </template>
    <v-date-picker
      v-model="form.value"
      @input="toggleMenu = false"
      no-title
      min="1950-01-01"
      :max="today"
    ></v-date-picker>
  </v-menu>
</template>
<script>
export default {
  props: {
    form: Object
  },
  data() {
    return {
      toggleMenu: false,
      today: new Date().toISOString().substr(0, 10),
      dateFormatted: ""
    };
  },
  methods: {
    formatDate(date) {
      if (!date) return null;

      const year = date.slice(0, 4);
      const month = date.slice(5, 7);
      const day = date.slice(8);
      return `${year}年${month}月${day}日`;
    },
  },
  watch: {
    'form.value': function(newVal) {
      this.dateFormatted = this.formatDate(newVal)
    }
  },
  created() {
    if (this.form.value) {
      this.dateFormatted = this.formatDate(this.form.value);
    } else {
      this.dateFormatted = this.formatDate(new Date().toISOString().substr(0, 10));    
    }
  },
};
</script>