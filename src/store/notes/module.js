import actions from './actions'
import mutations from './mutations'

const state = {
  note: '',
  notes: '',
}

const getters = {
  getNote(state) {
    return state.note
  },
  getNotes(state) {
    return state.notes
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
