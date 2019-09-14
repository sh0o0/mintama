//vue modules
import Vue from 'vue'
import router from '@/router/index'
import vuetify from '@/plugins/vuetify'
import store from '@/store'
//views
import Login from '@/views/Login'
import Logout from '@/views/Logout'
import Signup from '@/views/Signup'
import Baseline from '@/views/Baseline'
//css
import '@/../static/mintama/css/main.sass'


//set components
Vue.component('login-view', Login)
Vue.component('logout-view', Logout)
Vue.component('signup-view', Signup)
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