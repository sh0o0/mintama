<template>
  <div>
    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="gray" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
    <h2 class="font-weight-bold ">{{ note.title }}</h2>

    <v-row class="pa-2 ma2">
      <v-avatar size="40" class="ml-10">
        <v-img :src="user.icon" class="mr-2"></v-img>
        <span>{{ user.username }}</span>
      </v-avatar>
      <v-spacer></v-spacer>
      <router-link
        v-if="$route.params.username === getMyself.username"
        tag="div"
        :to="{name: 'updateNote', params: {username: $route.params.username, noteId: $route.params.noteId}}"
      >
        <v-btn color="amber" link>edit</v-btn>
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
        <v-card-title class="grey lighten-1">{{ section.heading}}</v-card-title>
        <v-card-text class="mb-3">{{ section.content }}</v-card-text>
        <v-row>
          <v-col class="d-inline-flex flex-row mb-2">
            <v-card
              v-for="(category, index) in section.categories_dict"
              :key="index"
              class="mx-1 pa-1 blue lighten-4"
              outlined
            >{{ category.name }}</v-card>
          </v-col>
        </v-row>

        <v-card class="d-inline-flex flex-row mb-2" flat tile>
          <v-card
            v-for="(reference, index) in section.references_dict"
            :key="index"
            class="mx-1"
          >{{ reference.title }}</v-card>
        </v-card>
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