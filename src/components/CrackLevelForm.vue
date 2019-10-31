<template>
  <div>
    <v-text-field 
    :label="form.label" 
    :value="form.value" 
    :prepend-icon="form.prependIcon"
    readonly 
    >
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
    <v-dialog v-model="crackChallengeDialog" max-width="400">
      <v-card>
        <v-card-title >レベルアップに挑戦！！！</v-card-title>

        <v-card-text>未実装</v-card-text>

        <v-card-actions>
          <div class="flex-grow-1"></div>

          <v-btn color="green darken-1" text @click="crackChallengeDialog = false">する</v-btn>

          <v-btn color="green darken-1" text @click="crackChallengeDialog = false">しない</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
export default {
  props: {
    form: Object,
  },
  data() {
    return {
      crackChallengeDialog: false,
    }
  },
}

</script>