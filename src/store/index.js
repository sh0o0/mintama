import Vue from 'vue'
import Vuex from 'vuex'

import accountsModule from './accounts/module'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    accounts: accountsModule,
  }
})