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

//遅延ローディング：　エラー計上のため保留
// const LoginOrSignup = import('@/views/LoginOrSignup') 
// const Logout = import('@/views/Logout') 
// const Baseline = import('@/views/Baseline') 
//
// Vue.config.errorHandler = (err, vm, info) => {
//     console.log(`Captured in Vue.config.errorHandler: ${info}`, err);
//   };
//   window.addEventListener("error", event => {
//     console.log("Captured in error EventListener", event.error);
//   });
//   window.addEventListener("unhandledrejection", event => {
//     console.log("Captured in unhandledrejection EventListener", event.reason);
//   });


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