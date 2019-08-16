import Vue from 'vue'
import Vuex from 'vuex'

import spots from './spots.module'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    spots
  }
})