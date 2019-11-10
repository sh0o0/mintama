<template>
  <div>
    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="grey" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
    <h2 class="font-weight-bold">{{ note.title }}</h2>

    <v-row class="pa-2 ma2">
      <router-link class="deco-none" :to="{name: 'profile', params: {username: user.username}}">
          <v-img v-if="user.icon" :src="user.icon" class="mr-2"/>
          <v-icon v-else large>mdi-egg</v-icon>

          <span>{{ user.username }}</span>
      </router-link>
      <v-spacer></v-spacer>
      <router-link
        v-if="$route.params.username === getMyself.username"
        tag="div"
        :to="{name: 'updateNote', params: {username: $route.params.username, noteId: $route.params.noteId}}"
      >
        <v-btn color="amber" class="mr-3" link>編集</v-btn>
      </router-link>
    </v-row>
    <v-divider></v-divider>
    <main class="mt-10">
      <v-card-title v-if="sectionCount() === 0">セクションはありません。</v-card-title>
      <v-card
        v-else
        v-for="(section, index) in note.sections"
        :key="index"
        class="mb-12 mx-2"
        flat
        outlined
        elevation="5"
      >
        <v-card-title class="grey lighten-1">{{ section.heading }}</v-card-title>
        <v-card-text class="mb-3" v-html="parseSection(section.content)"></v-card-text>
        <v-row>
          <v-col class="d-inline-flex flex-row mb-2">
            <v-card
              v-for="(category, index) in section.categories_dict"
              :key="index"
              class="mx-1 pa-1 blue lighten-4"
              outlined
              raised
            >{{ category.name }}</v-card>
          </v-col>
        </v-row>

        <v-col class="d-inline-flex flex-row mb-2 ma-0 pa-0">
          <router-link
            class="deco-none add-pointer"
            v-for="(reference, index) in section.references_dict"
            :key="index"
            :to="{name: 'personalReferenceList', params: {username: user.username}}"
          >
            <v-card class="mx-1 pa-1 green lighten-4" outlined raised>{{ reference.title }}</v-card>
          </router-link>
        </v-col>
      </v-card>
    </main>
  </div>
</template>

<script>
import FormatHelper from "@/helper/format";
import { Api } from "@/asynchronous/api";
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      note: {},
      user: "",
      isLoading: false,
      sectionsNum: 0
    };
  },
  methods: {
    sectionCount() {
      try {
        var count = this.note.sections.length;
      } catch (e) {
        return 0;
      }
      return count;
    },
    parseSection(text) {
      return text.replace(/\r?\n/g, '<br>')
    }
  },
  computed: {
    ...mapGetters("accounts", ["getMyself"])
  },
    created() {
    this.isLoading = true;
    const that = this;
    const noteId = this.$route.params.noteId;
    const username = this.$route.params.username;
    Api.getJson("notes", noteId, username)
      .then(response => {
        that.note = response.data;
        that.isLoading = false;
        Api.getJson("users", username).then(response => {
          that.user = response.data;
        });
      })
      .catch(error => {
        that.isLoading = false;
        alert("このノートは存在しません。");
      });
  }
};
</script>