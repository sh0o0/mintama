import axios from 'axios'
import Cookies from 'js-cookie'
import _ from 'lodash'
import Vue from 'vue'
import VueAxios from 'vue-axios'

import FormHelper from '@/helper/form'

const BASE_URL = 'http://127.0.0.1:8000/'

Vue.use(VueAxios, axios);
Vue.axios.defaults.baseURL = BASE_URL;

const isEmpty = obj => !Object.keys(obj).length

export const Rest = {
  get: (entries, slug='') => {
  return Vue.axios
      .get(`${entries}\/${slug}\/`)
      .catch((error) => {
        throw new Error(`ApiService ${error}`)
      })
  },
  post: (entries, formDatas, redirectUrl=null) => {
    const url = `${entries}\/`
    const csrftoken = Cookies.get('csrftoken');
    const headers = {'X-CSRFToken': csrftoken};
    const data = FormHelper.normalizesFormObj(formDatas);

    return Vue.axios.post(url, data, {headers: headers, 'Content-Type': 'multipart/form-data'})
    .then(function(response) {
      if (isEmpty(response.data) && redirectUrl !== null) {
        location.href = BASE_URL + redirectUrl
      } else {
        setErrors(formDatas, response.data)
      }
    })
    .catch(function(error) {
        throw new Error(`Api ${error}`);
    })
  },
  put: (entries, slug="", formData) => {
    const url = `${entries}\/${slug}\/`
    const csrftoken = Cookies.get('csrftoken');
    const headers = {'X-CSRFToken': csrftoken, 'Content-Type': 'multipart/form-data'};
    const data = FormHelper.createFormData(formData);

    return Vue.axios.put(url, data, {headers: headers})
    .then(function(response) {
      console.log('api put successe', response.data)
    })
    .catch(function(error) {
        throw new Error(`Api ${error}`);
    })
  },

  patch: (entries, slug="", formData) => {
    const url = `${entries}\/${slug}\/`
    const csrftoken = Cookies.get('csrftoken');
    const headers = {'X-CSRFToken': csrftoken, 'Content-Type': 'multipart/form-data'};
    const data = FormHelper.createFormData(formData);

    return Vue.axios.patch(url, data, {headers: headers})
    .then(function(response) {
      console.log('api patch successe', response.data)
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


const checkOneForm = (entries, formName, checkFormObjs) => {
  // const sliceIndex = location.href.indexOf('#/');
  // const href = location.href.slice(0, sliceIndex);
  const checkFormObj = checkFormObjs[formName];

  const url = `${entries}\/check_${formName}/`; 
  const data = {[formName]: checkFormObj.value};
  const csrftoken = Cookies.get('csrftoken');
  const headers = {'X-CSRFToken': csrftoken};

  Vue.axios.post(url, data, {headers: headers})
  .then(function(response) {
    if (isEmpty(response)) {
      checkFormObj.errors = [];
    } else {
      checkFormObj.errors = response.data[formName];
    }
  })
  .catch(function(error) {
    throw new Error(`checkOneForm ${error}`);
  })
}

export const debouncedCheckOneForm = _.debounce(checkOneForm, 1000)
