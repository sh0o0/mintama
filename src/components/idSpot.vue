<template>
  <div id="idSpot">
    <h1>{{ currentSpot.name }}</h1>
    <div class="description">
      <div>
        <p><span class="grey"> 名前 </span>{{ currentSpot.name }}</p>
        <p><span class="grey"> カテゴリー </span>{{ currentSpot.category }}</p>
        <p><span class="grey"> ジャンル </span>{{ currentSpot.genre }}</p>
        <p><span class="grey"> 都道府県 </span>{{ currentSpot.address_prefecture }}</p>
        <p><span class="grey"> 市区町村 </span>{{ currentSpot.address_city }}</p>
        <p><span class="grey"> 丁目番地等 </span>{{ currentSpot.address_street }}</p>
        <p><span class="grey"> 緯度 </span>{{ currentSpot.latitude }}</p>
        <p><span class="grey"> 経度 </span>{{ currentSpot.longitude }}</p>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    name: 'idSpot',
    computed: {
      ...mapGetters([
        'currentSpot',
        'isLoading'
      ])
    }
  }
</script>

<style scoped lang='sass'>
  h1
    text-transform: uppercase
    font-size: 40px
  .description
    width: 500px
    flex: 2
    padding: 10px 15px
    display: flex
    flex-direction: column
    justify-content: space-around
    div
      p
        text-transform: uppercase
        display: flex
        justify-content: space-between
        span
          font-size: 18px
          padding: 0 10px 0 0

</style>