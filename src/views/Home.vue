<template>
  <section class="container">
    <h1>スポット一覧</h1>
    <spotList></spotList>
    <redirectButton></redirectButton>
  </section>
</template>

<script>
  import redirectButton from '@/components/Button'
  import spotList from '@/components/SpotList'
  import { FETCH_SPOTS } from '@/store/actions.type'
  import { mapGetters } from 'vuex'

  export default {
    components: {
      redirectButton,
      spotList
    },
    
    mounted () {
      this.$store.dispatch(FETCH_SPOTS)
      .then(() => {
        console.log("YOU API");
      })
      .catch((err) => {
        console.log("ERR : ", err);
      })
    }
  }
</script>