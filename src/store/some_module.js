
const state = {
  counter: 0
}

const getters = {
  getCount(state) {
    return state.counter
  }
}

const actions = {
//   [FETCH_SPOTS](context, payload) {
//     context.commit(FETCH_START)
//     return ApiService
//       .get(`api/user`)
//       .then((response) => {
//         console.log('status:', response.status);
//         console.log('body:', response.data.results);
//         context.commit(SET_SPOTS, response.data.results);
//         context.commit(FETCH_END)
//       })
//       .catch((response) => {
//         context.commit(SET_ERROR, response.errors)
//       })
//   }
}

const mutations = {
  count(state) {
    state.counter++
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}

