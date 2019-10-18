import axios from "axios";
import Cookies from "js-cookie";
import Vue from "vue";
import VueAxios from "vue-axios";
import _ from "lodash";

import FormHelper from "@/helper/form";

const BASE_URL = "http://127.0.0.1:8000/";

Vue.use(VueAxios, axios);
Vue.axios.defaults.baseURL = BASE_URL;


const formatErrorResponse = error => {
  let ret = '';
  const errors = error.response.data
  for (let errorKey in errors) {
    ret += `■${errorKey}\n`
    for (let detail of errors[errorKey]) {
      ret += `　${detail}\n`
    }
  }
  return ret
}

export const Api = {
  get: (entries, slug = "") => {
    const url = `${entries}\/${slug + "/" ? slug : ""}`;
    return Vue.axios.get(url).catch(error => {
      throw new Error(`Api: ${error}`);
    });
  },
  post: (entries, formObj, token=null) => {
    const url = `${entries}\/`;
    let csrftoken = Cookies.get("csrftoken");
    if (!(csrftoken) && token) {
      csrftoken = token;
    }
    const headers = { 
      "X-CSRFToken": csrftoken,  
      "Content-Type": "multipart/form-data"
    };
    const data = FormHelper.createFormData(formObj);

    return Vue.axios
      .post(url, data, {
        headers: headers,
      })
      .catch(function(error) {
        throw new Error(`Api post ${error}`);
      });
  },
  put: (entries, slug, formData) => {
    const url = `${entries}\/${slug}\/`;
    const csrftoken = Cookies.get("csrftoken");
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "multipart/form-data"
    };
    const data = FormHelper.createFormData(formData);

    return Vue.axios
      .put(url, data, { headers: headers })
      .then(function(response) {
      })
      .catch(function(error) {
        throw new Error(`Api ${error}`);
      });
  },

  patch: (entries, slug, formObj) => {
    const url = `${entries}\/${slug}\/`;
    const csrftoken = Cookies.get("csrftoken");
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "multipart/form-data"
    };
    const data = FormHelper.createFormData(formObj);

    return Vue.axios
      .patch(url, data, { headers: headers })
      .then(function(response) {
      })
      .catch(function(error) {
        FormHelper.assignErrors(formObj, error.response.data);
        throw new Error(`Api ${error}`);
      });
  },

  delete: (entries, slug, username=null) => {
    let url;
    if (username) {
      url = `api/accounts/${username}/${entries}/${slug}/`;
    } else {
      url = `api/${entries}/${slug}/`;
    }

    const csrftoken = Cookies.get("csrftoken");
    const headers = { "X-CSRFToken": csrftoken };

    return Vue.axios
      .delete(url, { headers: headers })
      .then()
      .catch(function(error) {
        throw new Error(`Api delete${error}`);
      });
  },

  getJson: (entries, slug=null, username=null, options=null, method=null) => {
    let url;
    if (username) {
      url = `api/accounts/${username}/${entries}/`;
      if (slug) {
        url += `${slug}/`
      }
    } else {
      url = `api/${entries}/`;
      if (slug) {
        url += `${slug}/`
      }
    }

    if (method) {
      url += `${method}/`
    }

    if (options) {
      url += `?${options}`
    }

    return Vue.axios
      .get(url)
      .catch(function(error) {
        throw new Error(`Api getJson ${error}`);
      });
  },
  postJson: (entries, formData, username=null, options=null, method=null) => {
    let url;
    if (username) {
      url = `api/accounts/${username}/${entries}/`;
    } else {
      url = `api/${entries}\/`;
    }

    if (method) {
      url += `${method}/`
    }

    if (options) {
      url += `?${options}`
    }

    const csrftoken = Cookies.get("csrftoken");
    const headers = { 
      "X-CSRFToken": csrftoken ,
      "Content-Type": "application/json"
    };
    const data = FormHelper.createJsonFormData(formData);

    return Vue.axios
      .post(url, data, {
        headers: headers,
      })
      .catch(function(error) {
        alert('エラーが発生しました。')      
        // const formatedError = formatErrorResponse(error);
        // alert(formatedError);
        throw new Error(`Api postJson ${error}`);
      });
  },
  putJson: (entries, slug=null, formData, username=null, method=null) => {
    if (username) {
      var url = `api/accounts/${username}/${entries}/`;
    } else {
        var url = `api/${entries}/`;
    }

    if (slug) {
      url += `${slug}/`
    }

    if (method) {
      url += `${method}/`;
    }

    const csrftoken = Cookies.get("csrftoken");
    const headers = { 
      "X-CSRFToken": csrftoken ,
      "Content-Type": "application/json"
    };
    const data = FormHelper.createJsonFormData(formData);

    return Vue.axios
      .put(url, data, { headers: headers })
      .then()
      .catch(function(error) {
        alert('エラーが発生しました。')
        throw new Error(`Api putJson${error}`);
      });
  },

  patchJson: (entries, slug, formObj, username=null) => {
    let url;
    if (username) {
      url = `api/accounts/${username}/${entries}/${slug}/`;
    } else {
      url = `api/${entries}/${slug}/`;
    }
    const csrftoken = Cookies.get("csrftoken");
    const headers = { 
      "X-CSRFToken": csrftoken ,
      "Content-Type": "application/json"
    };
    const data = FormHelper.createJsonFormData(formObj);

    return Vue.axios
      .patch(url, data, { headers: headers })
      .then()
      .catch(error => {
        alert('エラーが発生しました。')
        throw new Error(`Api patchJson${error}`);
      });
  },
};

const checkOneForm = (entries, formName, checkFormObjs) => {
  // const sliceIndex = location.href.indexOf('#/');
  // const href = location.href.slice(0, sliceIndex);
  const checkFormObj = checkFormObjs[formName];

  const url = `${entries}\/check_${formName}/`;
  const data = { [formName]: checkFormObj.value };
  const csrftoken = Cookies.get("csrftoken");
  const headers = { "X-CSRFToken": csrftoken };

  Vue.axios
    .post(url, data, { headers: headers })
    .then(function(response) {
      if (FormHelper.isEmpty(response)) {
        checkFormObj.errors = [];
      } else {
        checkFormObj.errors = response.data[formName];
      }
    })
    .catch(function(error) {
      throw new Error(`checkOneForm ${error}`);
    });
};

export const debouncedCheckOneForm = _.debounce(checkOneForm, 1000);

export const API_MYSELF_URL = 'my!own!info'