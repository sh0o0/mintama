<template>
    <div>
        <a href="#" @click="apiUser">Button</a>
        <v-card>
            <v-card-title >{{ info }}</v-card-title>
            <v-card-text>aaaaaaaaaaaaaaaaaaa</v-card-text>
        </v-card>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
    methods: {
        ...mapActions([
            'apiUser'
        ]) ,
    },
    computed: {
        info() {
            return this.$store.getters.getInfo
        }
    }
}

</script>

<style scoped lang="sass">
a 
    display: block
    width: 100px
    height: 50px
    background-color: red
    text-align: center
    
</style>