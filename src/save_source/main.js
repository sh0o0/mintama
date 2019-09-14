//normal modules
import _ from 'lodash'
import Cookies from 'js-cookie'
//vue modules
import Vue from 'vue'
import router from '@/router/index'
import vuetify from '@/plugins/vuetify'
import store from '@/store/index'
//views
import App from '@/views/App'
import Login from '@/views/Login.vue'

//set components
Vue.component('second-temp', App)
Vue.component('login-view', Login)


let vm = new Vue({
    el: "#app-test",
    router,
    vuetify,
    store,
    data() {
        return {
            drawer: null,
            username: '',
            email: '',
            password1: '',
            password2: '',

            usernameErrors: [],
            emailErrors: [],
            password1Errors: [],
            password2Errors: [],
        }
    },
    created: function() {
      this.debouncedCheckOneForm = _.debounce(this.checkOneForm, 1000);
    },
    watch: {
      username: function() {
        this.debouncedCheckOneForm('username');
      },
      password1: function() {
        this.debouncedCheckOneForm('password1')
      },
    },
    methods: {
      checkOneForm: function(formName) {
        const url = `${location.href}check_${formName}/`; 
        const data = {[formName]: vm.$data[formName]};
        const csrftoken = Cookies.get('csrftoken');
        const headers = {'X-CSRFToken': csrftoken};

        Vue.axios.post(url, data, {headers: headers})
        .then(function(response) {
          if (response.data['available'] === true) {
            vm.$data[formName + 'Errors'] = [];
          } else {
            vm.$data[formName + 'Errors'] = response.data['errors'];
          }
        })
        .catch(function(error) {
          console.log(error);
        })
      }
    }
})