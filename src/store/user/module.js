import { RESIDENCE_CHOICIES, GENDER_CHOICIES } from './constant'

import actions from './actions'
import mutations from './mutations'

const state = {
  myself: '',
  baselineMyself: '',
  myselfOptionsAdded: '',
  userIsLoading: '',
  myselfError: '',
  inputImageData: '',
  loginOrSignup: 'Login',
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
  getIconSrc(state) {
    if (state.inputImageData){
      return state.inputImageData
    } else if (state.myself.icon) {
      return state.myself.icon
    } 
    return ''
  },
  getResidenceChoicies() {
    return RESIDENCE_CHOICIES
  },
  getGenderChoicies() {
    return GENDER_CHOICIES
  },
  getLoginOrSignup(state) {
    return state.loginOrSignup
  }
}


export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
