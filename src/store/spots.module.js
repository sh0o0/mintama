import ApiService from '@/services/api.service'
import {FETCH_A_SPOT, FETCH_SPOTS} from './actions.type'
import {FETCH_START, FETCH_END, SET_A_SPOT, SET_SPOTS, SET_ERROR} from './mutations.type'

const state = {
  spots: [],
  spot: {},
  loading: false
}

const getters = {
  currentSpot(state) {
    return state.spot
  },
  spots(state) {
    return state.spots
  },
  ifLoading(state) {
    return
  }
}

const actions = {
  [FETCH_SPOTS](context, payload) {
    context.commit(FETCH_START)
    return ApiService
      .get(`spots`)
      .then((response) => {
        console.log('status:', response.status);
        console.log('body:', response.data);
        context.commit(SET_SPOTS, response.data.spots);
        context.commit(FETCH_END)
      })
      .catch((response) => {
        context.commit(SET_ERROR, response.errors)
      })
  },
  [FETCH_A_SPOT](context, payload) {
    context.commit(FETCH_START)
    const {spot_id} = payload
    return ApiService
      .get(`spots/${spot_id}`)
      .then((response) => {
        console.log('status:', response.status);
        console.log('body:', response.data);
        context.commit(SET_A_SPOT, response.data.spots);
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
    state.spot = pSpot
    state.errors = {}
  },
  [SET_SPOTS](state, pSpots) {
    state.spots = pSpots
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

