<template>
    <v-dialog v-model="crackChallengeDialog" width="300">
      <v-card>
        <v-card-title class="headline">変更が完了しました。</v-card-title>

        <v-card-text>Let Google help apps determine location. This means sending anonymous location data to Google, even when no apps are running.</v-card-text>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn color="amber darken-1" text @click="crackChallengeDialog = false">しない</v-btn>

          <v-btn color="amber darken-1" text @click="crackChallengeDialog = false">する</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>
<script>
  export default {
    data() {
      return {
        crackChallengeDialog: false,
      }
    },
    computed: {
      ...mapState('user', ['myself'])
    }
  }

</script>