<template>
  <v-dialog 
  v-model="dialog" 
  @click:outside="dialogToFalse"
  width="300">
    <v-card>
      <v-card-title class="headline">{{ heading }}</v-card-title>

      <v-card-text>{{ content }}</v-card-text>

      <v-card-actions>
        <div class="flex-grow-1"></div>
        <v-btn color="amber darken-1" text @click="dialogToFalse">OK</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  props: {
    heading: String,
    content: String,
    dialog: Boolean
  },
  methods: {
    dialogToFalse() {
      this.$emit('dialog-to-false')
    } 
  }
};
</script>