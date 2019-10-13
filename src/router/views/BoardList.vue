<template>
  <div>
    <h2 class="font-weight-bold">{{ $route.params.username }} ボード一覧</h2>
    <v-divider></v-divider>

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
              class="deco-none mx-2"
              :to="{name: 'board', params: {username: username, boardId: board.id}}"
            >
              <v-btn color="amber" small>ボードに入る</v-btn>
            </router-link>
            <v-btn color="red" small @click.stop="confirmDialog = true; deleteBoardObj = board">削除</v-btn>
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

    <v-row class="bottom-btns">
      <v-btn
        link
        @click="formDialog = true; boardForm.name=''"
        class="blue-grey lighten-2 mr-2"
        fab
        dark
      >
        <v-icon dark>mdi-plus</v-icon>
      </v-btn>
    </v-row>

    <v-dialog v-model="formDialog" width="400">
      <v-card>
        <v-card-title class="headline">新規ボード作成</v-card-title>
        <v-card-actions>
          <v-text-field label="ボード名" v-model.trim="boardForm.name"></v-text-field>
        </v-card-actions>
        <v-divider></v-divider>
        <v-card-actions>
          <v-row class="mx-1">
            <v-btn text @click="createBoard">作成</v-btn>
            <v-btn text @click="formDialog = false">キャンセル</v-btn>
            <v-spacer></v-spacer>
            <v-btn class="grey lighten-4" text @click="createDefaultBoard()">デフォルトボードを作成</v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="confirmDialog" @click="confirmDialog = false" width="500">
      <v-card>
        <v-card-title class="headline">"{{ deleteBoardObj.name }}"を削除しますか？</v-card-title>
        <v-card-actions>
          <div class="flex-grow-1"></div>
          <v-btn
            color="gray darken-1"
            text
            @click="deleteBoard(deleteBoardObj.id); confirmDialog = false;"
          >する</v-btn>
          <v-btn color="gray darken-1" text @click="confirmDialog = false">しない</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="gray" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { Api } from "@/asynchronous/api";

export default {
  data() {
    return {
      username: this.$route.params.username,
      boards: [],
      isLoading: false,
      boardForm: {
        name: ""
      },
      confirmDialog: false,
      formDialog: false,
      deleteBoardObj: {}
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
    validateForm() {
      if (this.boardForm.name === "") return false;
      return true;
    },
    createBoard() {
      if (this.validateForm() === false) {
        alert("正しく入力してください");
        return;
      }
      this.isLoading = true;
      const that = this;
      const options = "include=id,name,lists";
      Api.postJson("boards", this.boardForm, this.username, options)
        .then(response => {
          that.boards.push(response.data);
          that.formDialog = false;
        })
        .finally(() => {
          that.isLoading = false;
        });
    },
    createDefaultBoard() {
      this.isLoading = true;
      const that = this;
      const options = "include=id,name,lists";
      Api.postJson("boards", null, this.username, options, "default")
        .then(response => {
          that.boards.push(response.data);
          that.formDialog = false;
        })
        .finally(() => {
          that.isLoading = false;
        });
    },
    deleteBoard(id) {
      this.isLoading = true;
      const that = this;
      Api.delete("boards", id, this.username)
        .then(response => {
          for (let i = 0; i < that.boards.length; i++) {
            if (that.boards[i].id === id) {
              that.boards.splice(i, 1);
              break;
            }
          }
        })
        .finally(() => {
          that.isLoading = false;
        });
    },
    init() {
      const that = this;
      this.retrieveBoards().then(response => {
        for (let board of that.boards) {
          for (let list of board.lists) {
            that.loadCards(list);
          }
        }
      });
    }
  },
  created() {
    this.init();
  }
};
</script>

<style scoped lang="sass">
.outline
  border: solid 1px gray
  border-radius: 10px
</style>