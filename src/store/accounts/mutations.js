export default {
  setMyself(state, payload) {
    state.myself = payload;
  },
  setUsername(state, username) {
    state.username = username;
  },
  setBaselineMyself(state) {
    state.baselineMyself = Object.assign({}, state.myself)
  },
  setMyselfError(state, error) {
    state.myselfError = error
  },
  setLogin(state) {
    state.loginOrSignup = 'Login'
  },
  setSignup(state) {
    state.loginOrSignup = 'Signup'
  },

  fetchStart(state) {
    state.userIsLoading = true
  },
  fetchEnd(state) {
    state.userIsLoading = false
  },
  setError(state, error) {
    state.myselfError = error
  }
}