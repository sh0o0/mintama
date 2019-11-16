<template>
  <div>
    <h2 class="font-weight-bold">{{ $route.params.username }} ノート一覧</h2>
    <router-link v-if="user" class="deco-none" :to="{name: 'profile', params: {username: user.username}}">
      <v-img v-if="user.icon" :src="user.icon" class="mr-2 user-icon" width="100"/>
      <v-icon v-else large>mdi-egg</v-icon>
    </router-link>
    <v-divider></v-divider>

    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="grey" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>

    <input type="text" v-model="searchValue" @input="searchRetrieveReferences" class="search-input" placeholder="Search">
    <main class="mt-2">
      <router-link
        class="deco-none"
        v-for="note in notes"
        :key="note.id"
        :to="{name: 'note', params: {username: note.username, noteId: note.id}}"
      >
      <transition name="fade" appear>
        <v-card class="mb-5 mx-2" outlined elevation="5">
          <v-card-title class="amber">{{ note.title }}</v-card-title>
          <v-card-text>
            <ul>
              <li
                class="my-1"
                v-for="(section, index) in note.sections"
                :key="index"
              >{{ section.heading }}</li>
            </ul>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions class="px-5">
            <v-row>
              <span>ユーザー: {{note.username}}</span>
              <v-spacer></v-spacer>
              <span>作成日時 : {{ note.written_at | datetimeToJapan }}</span>
            </v-row>
          </v-card-actions>
        </v-card>
      </transition>
      </router-link>
    </main>
    <v-row align="center" justify="center">
      <template>
        <v-btn v-if="next" link @click="fetchMore" class="gray lighten-2">MORE!</v-btn>
        <span v-else>NO MORE</span>
      </template>
    </v-row>
  </div>
</template>

<script>
import { dateToJapan, datetimeToJapan } from "@/helper/format";
import { Api, debounceGetJson } from "@/asynchronous/api";

export default {
  data() {
    return {
      notes: {},
      isLoading: false,
      next: '',
      user: "",
      searchValue: '',
    };
  },
  filters: {
    dateToJapan,
    datetimeToJapan
  },
  created() {
    this.fetch();
  },
  watch: {
    "$route.params.username": function() {
      this.notes = [];
      this.user = '';
      this.fetch();
    }
  },
  methods: {
    fetch() {
      this.isLoading = true;
      const that = this;
      const username = this.$route.params.username;

      if (username) {
        Api.getJson("users", username).then(response => {
          that.user = response.data;
        });
      };

      Api.getJson("notes", null, username).then(response => {
        that.notes = response.data.results;
        that.next = response.data.next;
      }).finally(() => {
        that.isLoading = false;
      });
    },
    fetchMore() {
      if (!(this.next)) return

      this.isLoading = true;
      const that = this;
      Api.normalGetJson(this.next).then(res => {
        that.notes.push(...res.data.results);
        that.next = res.data.next;        
      }).finally(() => {
        that.isLoading = false;
      });
    },
    searchRetrieveReferences() {
      const username = this.$route.params.username;
      const splitedComma = this.searchValue.trim().split(/\s+/).join(',')
      let options = null;
      if (splitedComma) {
        options = `q=${splitedComma}`
      }
      debounceGetJson('notes', this, 'notes', null, username, options)
    },
  }
};
</script>
<style scoped lang="sass">
.fade-enter-active, .fade-leave-active 
  transition: opacity 0.5s
.fade-enter, .fade-leave-to
  opacity: 0
</style>