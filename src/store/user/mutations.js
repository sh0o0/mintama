import { USER_OPTIONS } from '@/helper/constant'

export default {
  setMyself(state, payload) {
    state.myself = payload;
  },
  setBaselineMyself(state) {
    state.baselineMyself =  Object.assign({}, state.myself)
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
  setInputImageData(state, fileObj) {
    const fileReader = new FileReader()

    fileReader.onload = function() {
      state.inputImageData = this.result
      state.myself.icon = fileObj
    }
    fileReader.readAsDataURL(fileObj)
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