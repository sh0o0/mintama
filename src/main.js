//vue modules
import Vue from 'vue'
import router from '@/router/index'
import vuetify from '@/plugins/vuetify'
import store from '@/store'
//views
import LoginOrSignup from '@/views/LoginOrSignup'
import Logout from '@/views/Logout'
import Baseline from '@/views/Baseline'
//css
import '@/../static/mintama/css/main.sass'


//set components
Vue.component('login-or-signup', LoginOrSignup)
Vue.component('logout-view', Logout)
Vue.component('baseline-view', Baseline)


let vm = new Vue({
    el: "#app",
    router,
    vuetify,
    store,
    data() {
        return {
            
        }
    },
})