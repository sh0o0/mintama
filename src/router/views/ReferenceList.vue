<template>
  <div>
    <h2 class="font-weight-bold">{{ $route.params.username }} 参考資料</h2>
    <v-divider></v-divider>
    <input type="text" v-model="searchValue" @input="searchRetrieveReferences" class="search-input" placeholder="Search">
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
          <a :href="reference.link" target="_brank">リンク</a>
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
import { Api, debounceGetJson } from "@/asynchronous/api";

export default {
  data() {
    return {
      isLoading: false,
      references: [],
      referenceFormDialog: false,
      referenceForm: {origin: {}, form: {}},
      searchValue: '',
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
    searchRetrieveReferences() {
      let options = null;
      if (this.searchValue) {
        options = `q=${this.searchValue}`
      }
      const self = this;
      debounceGetJson('references', this, 'references', null, this.$route.params.username, options)
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
.search-input
  display: block
  width: 400px
  height: 50px
  margin-top: 5px
  padding: 3px
  border-radius: 20px
  border: 1px solid #000080
  outline: none
  font-size: 1.2rem
  transition: 0.4s
.search-input:focus,
.search-input:hover
  opacity: 0.8
  border: 2px solid #0099FF
  box-shadow: 2px 2px 2px 2px rgba(192, 192, 192, 0.5)
</style>