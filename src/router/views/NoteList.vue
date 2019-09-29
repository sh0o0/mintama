<template>
  <div>
    <h2 class="font-weight-bold">{{ $route.params.username }} ノート一覧</h2>
    <router-link
    class="deco-none"
    :to="{name: 'profile', params: {username: user.username}}"
    >
    <v-avatar size="40" v-if="user" class="ml-9 my-5">
      <v-img :src="user.icon" class="mr-2"></v-img>
      <span>{{ user.username }}</span>
    </v-avatar>
    </router-link>
    <v-divider></v-divider>

    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="gray" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-row>
      <v-col cols="6" md="3"></v-col>
    </v-row>
    <main>
      <router-link
        class="deco-none"
        v-for="(note, index) in notes"
        :key="index"
        :to="{name: 'note', params: {username: note.username, noteId: note.id}}"
      >
        <v-card class="mb-5 mx-2" outlined elevation="5">
          <v-card-title class="amber">{{ note.title }}</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item-content
                class="py-0"
                v-for="(section, index) in note.sections"
                :key="index"
                dence
              >・{{ section.heading }}</v-list-item-content>
            </v-list>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions class="px-5">
            <v-row>
              <span>user: {{note.username}}</span>
              <v-spacer></v-spacer>
              <span>作成日時 : {{ note.written_at | dateFormat }}</span>
            </v-row>
          </v-card-actions>
        </v-card>
      </router-link>
    </main>
    <v-row align="center" justify="center">
    
    <template>
    <v-btn v-if="next" link @click="fetch" class="gray lighten-2">
      more
    </v-btn>
    <span v-else>no more</span>
    </template>
    </v-row>
  </div>
</template>

<script>
import FormatHelper from "@/helper/format";
import { Api } from "@/asynchronous/api";


export default {
  data() {
    return {
      notes: {},
      isLoading: false,
      offset: 0,
      next: null,
      user: '',
    };
  },
  filters: {
    dateFormat(date) {
      return FormatHelper.dateToJp(date);
    }
  },
  created() {
    this.fetch();
  },
  methods: {
    fetch() {
      this.isLoading = true;
      const that = this;
      const username = this.$route.params.username

      Api.getJson("notes", null, username,`offset=${this.offset}`).then(response => {
        if (that.offset === 0) {
          that.notes = response.data.results;
        } else {
          that.notes.push(...response.data.results);
        };
        that.offset += 10;
        that.next = response.data.next
        that.isLoading = false;
        if (username) {
          Api.getJson("users", username).then(response => {
            that.user = response.data;
          });
        }
      });
    },
  }
};
</script>