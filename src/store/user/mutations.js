import { USER_OPTIONS } from './constant'

export default {
  setMyself(state, payload) {
    state.myself = payload;
  },
  setBaselineMyself(state, data) {
    state.baselineMyself = data
  },
  setMyselfError(state, error) {
    state.myselfError = error
  },
  setMyselfOptionsAdded(state, exclude) {
    state.myselfOptionsAdded = [];
    for(let key in state.myself) {
      if (exclude.includes(key)) {
        continue
      }
      let itemOptionAdded = {
        name: key, 
        value: state.myself[key], 
        label: USER_OPTIONS[key]
      }
      state.myselfOptionsAdded.push(itemOptionAdded)
    }
  },
  fetchStart(state) {
    state.userIsLoading = true
  },
  fetchEnd(state) {
    state.userIsLoading = false
  },
}