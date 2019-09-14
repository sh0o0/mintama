import { RESIDENCE_CHOICIES, GENDER_CHOICIES } from './constant'

import actions from './actions'
import mutations from './mutations'

const state = {
  myself: '',
  baselineMyself: '',
  myselfOptionsAdded: '',
  userIsLoading: '',
  myselfError: '',
}

const getters = {
  getMyself(state) {
    return state.myself
  },
  getMyselfOptionsAdded(state) {
    return state.myselfOptionsAdded
  },
  getMyselfError(state) {
    return state.myselfError
  },
  getResidenceChoicies() {
    return RESIDENCE_CHOICIES
  },
  getGenderChoicies() {
    return GENDER_CHOICIES
  }
}


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
