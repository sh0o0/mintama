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
        @blur="dateFormatted = formatDate(myself.learning_started_date)"
        label="学習開始時期"
        prepend-icon="event"
        v-on="on"
        readonly
      ></v-text-field>
    </template>
    <v-date-picker
      v-model="myself.learning_started_date"
      @input="toggleMenu = false"
      no-title
      min="1950-01-01"
      :max="today"
    ></v-date-picker>
  </v-menu>
  
</template>
<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      toggleMenu: false,
      today: new Date().toISOString().substr(0, 10),
      dateFormatted: '',
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
    parseDate(date) {
      if (!date) return null;

      const year = date.slice(0, 4);
      const month = date.slice(5, 7);
      const day = date.slice(8);
      return `${year}-${month}-${day}`;
    }
  },
  created() {
    this.$store.watch(
      (state, getters) => state.user.myself.learning_started_date,
      (newvalue, oldvalue) => {
        if (this.$store.state.user.myself.learning_started_date) {
          this.dateFormatted = this.formatDate(this.$store.state.user.myself.learning_started_date);
          return
        }
          this.formatDate = this.formatDate(new Date().toISOString().substr(0, 10))
      }
    )
  },
  computed: {
    ...mapState('user', ['myself']),
  }
};
</script>