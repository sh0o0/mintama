<template>
  <div>
    <v-text-field readonly label="ひび割れ度" :value="myself.crack_level" prepend-icon="mdi-egg-easter">
      <v-btn
        link
        color="red lighten-1"
        slot="append"
        text
        icon
        large　@click.stop="crackChallengeDialog = true"
      >
        <v-icon>mdi-alert-decagram</v-icon>
      </v-btn>
    </v-text-field>
    <v-dialog v-model="crackChallengeDialog" max-width="290">
      <v-card>
        <v-card-title class="headline">レベルアップに挑戦！！！</v-card-title>

        <v-card-text>Let Google help apps determine location. This means sending anonymous location data to Google, even when no apps are running.</v-card-text>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn color="green darken-1" text @click="crackChallengeDialog = false">しない</v-btn>

          <v-btn color="green darken-1" text @click="crackChallengeDialog = false">する</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
  import { mapState } from 'vuex'
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