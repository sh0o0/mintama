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
  setInputImageData(state, data) {
    console.log(data)
    const fileReader = new FileReader()

    fileReader.onload = function() {
      state.inputImageData = this.result
      state.myself.icon = data
    }
    fileReader.readAsDataURL(data)
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