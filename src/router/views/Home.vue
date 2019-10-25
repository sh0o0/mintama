<template>
  <div>
    <h2 class="font-weight-bold">ホーム</h2>
    <v-divider></v-divider>
    <main class="wrapper">
      <div class="left">
        <DispersionLearning></DispersionLearning>
      </div>
      <div class="right">
        <transition name="fade" mode="out-in">
        <Board
          v-if="isShowBoard"
          :homeDefaultBoard="own['default_board']"
          :homeUsername="own['username']"
          @show-not-board="isShowBoard = false"
          @delete-default-board="own['default_board'] = null; isShowBoard = false"
        ></Board>
        <HomeNotBoard 
        v-else 
        :homeDefaultBoard="own['default_board']"
        @show-default-board="isShowBoard = true"
        @load="retrieveUser()"
        ></HomeNotBoard>
        </transition>
      </div>
    </main>
  </div>
</template>
<script>
import { Api } from "@/asynchronous/api";
import Board from "@/router/views/Board";
import HomeNotBoard from "@/components/HomeNotBoard";
import DispersionLearning from "@/components/DispersionLearning";

export default {
  data() {
    return {
      own: {},
      isShowBoard: false
    };
  },
  components: {
    Board,
    HomeNotBoard,
    DispersionLearning,
  },
  methods: {
    retrieveUser() {
      const self = this;
      Api.getJson("own", "user").then(response => {
        self.own = response.data;
        self.isShowBoard = !!self.own["default_board"];
      });
    }
  },
  created() {
    this.retrieveUser();
  }
};
</script>
<style scoped lang="sass">
.wrapper
  margin-top: 10px
.left
  display: inline-block
  width: 47%
  margin: 0px auto 0px 0px
  vertical-align: top
  border: solid 1px rgba(192, 192, 192, 0.2)
.right
  display: inline-block
  width: 48%
  margin: 0px 0px 0px 3%
  border: solid 1px rgba(192, 192, 192, 0.2)
  width: 500px
.fade-enter-active, .fade-leave-active 
  transition: opacity 0.2s
.fade-enter, .fade-leave-to
  opacity: 0
@media screen and (max-device-width: 480px)
  .wrapper
    overflow-x: scroll
  .left
    width: 100%
  .right
    width: 100%

</style>