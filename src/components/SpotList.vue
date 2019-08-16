<template>
  <ul id="spotList">
    <li v-for="spot in spots">
      <div class="description">
        <p><span class="grey"> 名前 </span>{{ spot.name }}</p>
        <p><span class="grey"> カテゴリー </span>{{ spot.category }}</p>
        <p><span class="grey"> 都道府県 </span>{{ spot.address_prefecture }}</p>
      </div>
    </li>
  </ul>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    name: 'spotList',
    computed: {
      ...mapGetters([
        'spots',
        'isLoading'
      ])
    }
  }
</script>

<style scoped lang='sass'>
  #spotList
    min-width: 85%
    li
      list-style: none
      width: 500px
      display: flex
      justify-content: space-between
      border: solid 3px #e0e0e0
      margin: 15px 0
      box-shadow: 2px 3px #adadad
      .description
        flex: 2
        padding: 10px 15px
        background: #f5f5f5
        p
          text-transform: uppercase
          span
            font-size: 18px
            color: darkgrey
            padding: 0 10px 0 0
</style>