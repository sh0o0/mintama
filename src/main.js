import _ from 'lodash'
import Vue from 'vue'
import router from '@/router'

import App from './App.vue'

import 'vuetify/dist/vuetify.min.css'


Vue.component('second-temp', App)

new Vue({
    el: "#app-test",
    router,
    data() {
        return {
            message: 'aaaaa'
        }
    },
})