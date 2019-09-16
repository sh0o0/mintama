<template>
  <v-app>
    <v-card class="pa-2 pb-8">
      <v-card-title>日記を書く</v-card-title>

      <v-card v-for="(section, index) in diary.sections" :key="index" class="pa-2 py-5">
        <v-card-title>
          <v-text-field
          
          />
        </v-card-title>
        <v-col cols="12" md="9"></v-col>
      </v-card>

      <v-col cols="12" md="9"></v-col>
    </v-card>
  </v-app>
</template>
<script>
export default {
  data() {
    return {
      diary: {
        title: "",
        sections: []
      }
    };
  },
  methods: {
    addSection() {
      const section = {
        heading: "",
        categories: [],
        content: "",
        references: []
      };
      this.diary.sections.push(section);
    }
  },
  created() {
    this.addSection();
  }
};
</script>