<template>
  <div>
    <h2 class="font-weight-bold">{{ $route.params.username }} 参考資料</h2>
    <v-divider></v-divider>

    <v-list>
      <v-list-group
        v-for="reference in references"
        :key="reference.id"
        :value="false"
        class="reference"
      >
        <template v-slot:activator>
          <v-row>
            <h3 class="font-weight-bold">{{ reference.title }}</h3>
            <v-spacer></v-spacer>
            <div v-if="$route.params.username === getBaselineMyself.username">
              <v-btn
                @click.stop="referenceFormDialog = true; referenceForm.origin = reference; referenceForm.form = Object.assign({}, reference)"
                class="deco-none mx-2 amber"
                small
              >編集</v-btn>
              <v-btn
                class="deco-none mx-2 red"
                @click.stop="deleteReferenceDialog = true; deleteTargetReference = reference"
                small
              >削除</v-btn>
            </div>
          </v-row>
        </template>

        <v-list-item class="pl-2">
          <router-link
            class="deco-none"
            :to="{name: 'profile', params: {username: reference.username}}"
          >
            <v-icon>mdi-egg</v-icon>
            <span class="amber--text">{{ reference.username }}</span>
          </router-link>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>{{ reference.content }}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <a :href="reference.link" target="_brank">{{ reference.link }}</a>
        </v-list-item>
      </v-list-group>
    </v-list>

    <v-row class="bottom-btns">
      <v-btn
        @click="referenceFormDialog = true; referenceForm.form = {}"
        link
        class="mr-2 grey"
        fab
        dark
      >
        <v-icon dark>mdi-plus</v-icon>
      </v-btn>
    </v-row>

    <v-dialog v-model="referenceFormDialog" width="600">
      <v-card class="pa-2">
        <v-card-title class="headline">新しいリファレンスの作成</v-card-title>
        <v-card-actions>
          <v-text-field label="名前" v-model.trim="referenceForm.form.title"></v-text-field>
        </v-card-actions>

        <v-card-actions>
          <v-textarea label="内容" v-model.trim="referenceForm.form.content"></v-textarea>
        </v-card-actions>

        <v-card-actions>
          <v-text-field type="url" label="リンク" v-model.trim="referenceForm.form.link"></v-text-field>
        </v-card-actions>

        <v-card-actions>
          <v-row class="mx-1">
            <v-spacer></v-spacer>
            <v-btn v-if="referenceForm.form.id" text @click="updateReference()">変更</v-btn>
            <v-btn v-else text @click="createReference()">作成</v-btn>
            <v-btn text @click="referenceFormDialog = false">キャンセル</v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteReferenceDialog" width="400">
      <v-card>
        <v-card-title>"{{ deleteTargetReference.title }}"を削除しますか？</v-card-title>
        <v-card-actions>
          <v-row class="mx-1">
            <v-spacer></v-spacer>
            <v-btn text @click="deleteReference()">削除</v-btn>
            <v-btn text @click="deleteReferenceDialog = false">キャンセル</v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="grey" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import { Api } from "@/asynchronous/api";

export default {
  data() {
    return {
      isLoading: false,
      references: [],
      referenceFormDialog: false,
      referenceForm: {origin: {}, form: {}},
      deleteReferenceDialog: false,
      deleteTargetReference: {}
    };
  },
  computed: {
    ...mapGetters("accounts", ["getBaselineMyself"])
  },
  methods: {
    retrieveReferences() {
      this.isLoading = true;
      const self = this;
      Api.getJson("references", null, this.$route.params.username)
        .then(response => {
          self.references = response.data.results;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    createReference() {
      this.isLoading = true;
      const self = this;
      Api.postJson(
        "references",
        this.referenceForm.form,
        this.$route.params.username
      )
        .then(response => {
          self.references.push(response.data);
          self.referenceFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    updateReference() {
      this.isLoading = true;
      const self = this;
      Api.putJson(
        "references",
        this.referenceForm.origin.id,
        this.referenceForm.form,
        this.$route.params.username
      )
        .then(response => {
          const resData = response.data;
          for (const key in resData) {
            self.referenceForm.origin[key] = resData[key];
          };
          self.referenceFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    deleteReference() {
      this.isLoading = true;
      const self = this;
      Api.delete(
        "references",
        this.deleteTargetReference.id,
        this.$route.params.username
      )
        .then(response => {
          self.eraseReference(self.deleteTargetReference);
          self.deleteReferenceDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    eraseReference(reference) {
      const referencesLen = this.references.length;
      for (let i = 0; i < referencesLen; i++) {
        if (this.references[i].id === reference.id) {
          this.references.splice(i, 1);
          return;
        }
      }
    }
  },
  watch: {
    "$route.params.username": function() {
      this.retrieveReferences();
    }
  },
  created() {
    this.retrieveReferences();
  }
};
</script>
<style scoped lang="sass">
.reference
  border: 1px solid orange
</style>