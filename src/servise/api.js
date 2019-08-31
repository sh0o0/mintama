import Vue from 'vue'
import VueAxios from 'vue-axios'

const ApiService = {
  init () {
    Vue.use(VueAxios, axios);
    Vue.axios.defaults.baseURL = API_URL;
  },

  get (resource, slug='') {
    return axios
      .get(`${resource}\\${slug}`)
      .catch((error) => {
        throw new Error(`ApiService ${error}`)
      })
  },
}

export default ApiService