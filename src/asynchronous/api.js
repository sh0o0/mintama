import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Cookies from 'js-cookie'

const API_URL = 'http://127.0.0.1:8000/'

Vue.use(VueAxios, axios);
Vue.axios.defaults.baseURL = API_URL;

export default {
  get: (entries, slug='') => {
  return Vue.axios
      .get(`${entries}\/${slug}\/`)
      .catch((error) => {
        throw new Error(`ApiService ${error}`)
      })
  },
  post: (entries, data) => {
    const url = `${entries}\/`
    const csrftoken = Cookies.get('csrftoken');
    const headers = {'X-CSRFToken': csrftoken};

    return Vue.axios.post(url, data, {headers: headers})
    .then(function(response) {
      console.log('user post successe')
    })
    .catch(function(error) {
        throw new Error(`Api ${error}`);
    })
  },
  put: (entries, slug="", data) => {
    const url = `${entries}\/${slug}\/`
    const csrftoken = Cookies.get('csrftoken');
    const headers = {'X-CSRFToken': csrftoken, 'Content-Type': 'multipart/form-data'};

    const formData = new FormData();
    for (let formKey in data) {
      if (formKey === 'icon' && typeof data[formKey] === 'string') continue
      formData.append(formKey, data[formKey])
    } 

    return Vue.axios.put(url, formData, {headers: headers})
    .then(function(response) {
      console.log('user put successe')
    })
    .catch(function(error) {
        throw new Error(`Api ${error}`);
    })
  },
  delete: (entries, slug="") => {
    const url = `${entries}\/${slug}\/`
    const csrftoken = Cookies.get('csrftoken');
    const headers = {'X-CSRFToken': csrftoken};

    return Vue.axios.delete(url, data, {headers: headers})
    .then(function(response) {
      console.log('user delete successe')
    })
    .catch(function(error) {
        throw new Error(`Api ${error}`);
    })
  },
}