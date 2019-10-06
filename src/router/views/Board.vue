<template>
  <div>
    <h2 class="font-weight-bold">{{ borad.name }}</h2>
    <v-divider></v-divider>

    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="gray" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-list class="outline">
      <v-list-group
        v-for="(board, boardIndex) in boards"
        :key="board.name + boardIndex"
        :value="false"
        class="outline my-3"
      >
        <template v-slot:activator>
          <v-row class="px-2">
            <h3 class="font-weight-bold">{{ board.name }}</h3>
            <v-spacer></v-spacer>
            <router-link
              class="deco-none"
              :to="{name: 'board', params: {username: $route.params.username, boardId: board.id}}"
            >
              <v-btn color="amber" small>ボードに入る</v-btn>
            </router-link>
          </v-row>
        </template>

        <v-list-group
          v-for="(list, listIndex) in board.lists"
          :key="list.name + listIndex"
          no-action
          sub-group
          :value="false"
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title>{{ list.name }}</v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item v-for="(card, cardIndex) in list.cards" :key="card.name + cardIndex" link>
            <v-list-item-title>{{ card.name }}</v-list-item-title>
          </v-list-item>
        </v-list-group>
      </v-list-group>
    </v-list>
  </div>
</template>
<script>
import { Api } from "@/asynchronous/api";

export default {
  data() {
    return {
      username: this.$route.params.username,
      boards: [],
      lists: [],
      isLoading: false,
      boardForm: {
        name: ""
      },
      confirmDialog: false
    };
  },
  computed: {
    cards() {
      return this.retrieveCard;
    }
  },
  methods: {
    retrieveBoards() {
      this.isLoading = true;
      const that = this;
      const options = "include=id,name,lists";
      return Api.getJson("boards", null, this.username, options)
        .then(response => {
          that.boards = response.data.results;
          that.isLoading = false;
        })
        .catch(error => {
          alert("データが正しく取得できませんでした。");
          that.isLoading = false;
        });
    },
    loadCards(list) {
      const that = this;
      const options = "include=name,cards";
      return Api.getJson("lists", list.id, this.username, options).then(
        response => {
          that.$set(list, "cards", response.data.cards);
        }
      );
    },
    createBoard() {
      this.isLoading = true;
      const that = this;
      Api.postJson("boards", this.boardForm, this.username).then(response => {
        that.boards.push(response.data);
        that.confirmDialog = true;
        that.isLoading = true;
      });
    },
    pageTransition(boardId) {
      this.$router.push({
        name: "board",
        params: { username: this.username, boardId: boardId }
      });
    }
  },
  created() {
    const that = this;
    this.retrieveBoards().then(response => {
      for (let board of that.boards) {
        for (let list of board.lists) {
          that.loadCards(list);
        }
      }
    });
  }
};
</script>