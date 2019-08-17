import ApiService from '@/services/api.service'
import {FETCH_A_SPOT, FETCH_SPOTS} from './actions.type'
import {FETCH_START, FETCH_END, SET_A_SPOT, SET_SPOTS, SET_ERROR} from './mutations.type'

const state = {
  users: [],
  user: {},
  loading: false
}

const getters = {
  currentSpot(state) {
    return state.user
  },
  users(state) {
    return state.users
  },
  ifLoading(state) {
    return loading
  }
}

const actions = {
  [FETCH_SPOTS](context, payload) {
    context.commit(FETCH_START)
    return ApiService
      .get(`api/user`)
      .then((response) => {
        console.log('status:', response.status);
        console.log('body:', response.data.results);
        context.commit(SET_SPOTS, response.data.results);
        context.commit(FETCH_END)
      })
      .catch((response) => {
        context.commit(SET_ERROR, response.errors)
      })
  },
  [FETCH_A_SPOT](context, payload) {
    context.commit(FETCH_START)
    const {user_id} = 1 //payload
    return ApiService
      .get(`api/user/${user_id}`)
      .then((response) => {
        console.log('status:', response.status);
        console.log('body:', response);
        context.commit(SET_A_SPOT, response.data.users);
        context.commit(FETCH_END)
      })
      .catch(((response) => {
        context.commit(SET_ERROR, response.errors)
      }))
  }
}

const mutations = {
  [FETCH_START](state) {
    state.loading = true
  },
  [FETCH_END](state) {
    state.loading = false
  },
  [SET_A_SPOT](state, pSpot) {
    state.user = pSpot
    state.errors = {}
  },
  [SET_SPOTS](state, users) {
    state.users = users
    state.errors = {}
  },
  [SET_ERROR](state) {
    state.errors = errors
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}

