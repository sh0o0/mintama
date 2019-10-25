<template>
  <div>
    <h2 class="title font-weight-bold">ホームボード設定</h2>

    <div class="wrapper">
      <transition name="slide-fade" mode="out-in">
        <div v-if="isShowBoardList" class="board-list">
          <select class="board-select" v-model="selectedBoard">
            <option value></option>
            <option
              v-for="(board, index) in boardList"
              :key="index"
              :value="board.id"
            >{{ board.name }}</option>
          </select>
          <div>
            <a class="board-btn left deco-none" @click.stop="registerDefaultBoard()">確定</a>
            <a class="board-btn right deco-none" @click.stop="isShowBoardList = false">キャンセル</a>
          </div>
        </div>
        <a
          v-else
          class="btn deco-none"
          @click="isShowBoardList = true; retirieveBoardList()"
        >ホームに表示させるボード選択する</a>
      </transition>

      <a
        v-if="homeDefaultBoard"
        class="btn deco-none thin"
        @click="$emit('show-default-board')"
      >デフォルトボードの表示</a>

      <router-link
        class="btn deco-none under"
        :to="{name: 'boardList', params: {username: getBaselineMyself.username}}"
      >ボード一覧を見る</router-link>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import { Api } from "@/asynchronous/api";

export default {
  props: {
    homeDefaultBoard: Number
  },
  data() {
    return {
      boardList: [],
      isShowBoardList: false,
      selectedBoard: this.homeDefaultBoard
    };
  },
  computed: {
    ...mapGetters("accounts", ["getBaselineMyself"])
  },
  methods: {
    retirieveBoardList() {
      const username = this.getBaselineMyself.username;
      const options = "include=id,name";
      const self = this;
      Api.getJson("boards", null, username, options).then(response => {
        self.boardList = response.data.results;
      });
    },
    registerDefaultBoard() {
      const username = this.getBaselineMyself.username;
      const defaultBoardId = this.selectedBoard;
      const data = { default_board: defaultBoardId };
      const self = this;
      Api.patchJson("users", username, data).then(response => {
        self.$emit("load");
        alert("変更しました。");
      });
    }
  }
};
</script>
<style scoped lang="sass">
.wprapper
  text-align: center
.title
  text-align: center
a
  transition: 0.8s
a:hover
  opacity: 0.7
.board-list
  height: 120px
  text-align: center
.board-select
  display: block
  width: 300px
  height: 50px
  margin: 10px auto
  padding: 5px
  border: solid 1px #FFCC66
  border-radius: 10px
  font-size: 1.2rem
  font-weight: bold
.board-btn
  display: inline-block
  width: 100px
  height: 50px
  margin: 0px 40px
  line-height: 50px
  border-radius: 10px
  box-shadow: 2px 2px 3px 1px rgba(192, 192,192 ,0.8)
.board-btn.left
  background-color: rgba(255,153,102, 0.5)
.board-btn.right
  background-color: rgba(230, 230, 230, 0.5)
.btn
  display: block
  width:  300px
  height: 100px
  margin: 20px auto
  background-color: rgba(192,192, 192, 0.5)
  border: solid 2px #C0C0C0
  border-radius: 20px
  box-shadow: 3px 3px 5px 5px rgba(192, 192,192 ,0.4)
  line-height: 90px
  text-align: center
.btn.thin
  height: 50px
  background-color: rgba(230, 230, 230 ,0.4)
  line-height: 50px
.under
  margin-top: 100px
.slide-fade-enter-active, .slide-fade-leave-active 
  // transform: translate(0px, 0px)
  transition: opacity 225ms
  // transition: transform 225ms opacity 225ms cubic-bezier(0, 0, 0.2, 1) 0ms
.slide-fade-enter, .slide-fade-leave-to
  // transform: translateY(-5vh)
  opacity: 0

</style>