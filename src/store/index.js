import Vue from 'vue'
import Vuex from 'vuex'

import some from './some_module'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    some
  }
})