import Vue from 'vue'
import Vuex from 'vuex'

import accountsModule from './accounts/module'
import diariesModule from './diaries/module'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    accounts: accountsModule,
    diaries: diariesModule,
  }
})