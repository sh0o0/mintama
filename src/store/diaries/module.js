import actions from './actions'
import mutations from './mutations'

const state = {
  diary: '',
  diaries: '',
}

const getters = {
  getDiary(state) {
    return state.diary
  },
  getDiaries(state) {
    return state.diaries
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
