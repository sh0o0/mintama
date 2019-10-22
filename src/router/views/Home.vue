<template>
  <div class="wrapper">
    <h2 class="font-weight-bold">ホーム</h2>
    <v-divider></v-divider>
    <section class="left">
    <h3>ウォズニアック式勉強</h3>

    </section>
    <section class="right">
    <h3>デフォルトボード</h3>
    <Board></Board>
    </section>
    

</div>
</template>
<script>
import Board from '@/router/views/Board'

export default {
  data(){
    return {

    };
  },
  components: {
    Board,
  },
}
</script>
<style scoped lang="sass">
.left
  display: inline-block
  width: 49%
  margin-left: 0px
  vertical-align: top
.right
  display: inline-block
  width: 49%
  margin-right: 0px
.board
  height: 500px
  width: 500px
@media screen and (max-device-width: 480px)
  .wrapper
    overflow-x: scroll
  .left
    width: 450px
  .right
    width: 450px
</style>