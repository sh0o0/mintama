import axios from "axios";
import Cookies from "js-cookie";
import Vue from "vue";
import VueAxios from "vue-axios";
import _ from "lodash";

import FormHelper from "@/helper/form";

const BASE_URL = "http://127.0.0.1:8000/";

Vue.use(VueAxios, axios);
Vue.axios.defaults.baseURL = BASE_URL;

// const formatErrorResponse = error => {
//   let ret = '';
//   const errors = error.response.data
//   for (let errorKey in errors) {
//     ret += `■${errorKey}\n`
//     for (let detail of errors[errorKey]) {
//       ret += `　${detail}\n`
//     }
//   }
//   return ret
// }

const generateUrl = ({
  entries = null,
  slug = null,
  username = null,
  options = null,
  method = null,
  isApi = true
}) => {
  let url = "";
  if (isApi) {
    url = "api/";
  }

  if (username) {
    url += `accounts/${username}/${entries}/`;
  } else {
    url += `${entries}/`;
  }

  if (slug) {
    url += `${slug}/`;
  }

  if (method) {
    url += `${method}/`;
  }

  if (options) {
    url += `?${options}`;
  }

  return url;
};

const Api = {
  get: (entries, slug = "") => {
    const url = generateUrl({ entries: entries, slug: slug });
    return Vue.axios.get(url);
  },
  post: (entries, formObj, token = null, isApi = true) => {
    const url = generateUrl({ entries: entries, isApi: isApi });
    let csrftoken = Cookies.get("csrftoken");
    if (!csrftoken && token) {
      csrftoken = token;
    }
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "multipart/form-data"
    };
    const data = FormHelper.createFormData(formObj);

    return Vue.axios
      .post(url, data, {
        headers: headers
      })
      .catch(function(error) {
        throw error;
      });
  },
  put: (entries, slug, formData) => {
    const url = generateUrl({ entries: entries, slug: slug });
    const csrftoken = Cookies.get("csrftoken");
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "multipart/form-data"
    };
    const data = FormHelper.createFormData(formData);

    return Vue.axios
      .put(url, data, { headers: headers })
      .then(function(response) {})
      .catch(function(error) {
        throw new Error(`Api ${error}`);
      });
  },

  patch: (entries, slug, formObj) => {
    const url = generateUrl({ entries: entries, slug: slug });
    const csrftoken = Cookies.get("csrftoken");
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "multipart/form-data"
    };
    const data = FormHelper.createFormData(formObj);

    return Vue.axios
      .patch(url, data, { headers: headers })
      .then(function(response) {})
      .catch(function(error) {
        FormHelper.assignErrors(formObj, error.response.data);
        throw error;
      });
  },

  delete: (entries, slug, username = null) => {
    const url = generateUrl({
      entries: entries,
      slug: slug,
      username: username
    });
    const csrftoken = Cookies.get("csrftoken");
    const headers = { "X-CSRFToken": csrftoken };

    return Vue.axios
      .delete(url, { headers: headers })
      .then()
      .catch(function(error) {
        throw new Error(`Api delete ${error}`);
      });
  },

  getJson: (
    entries,
    slug = null,
    username = null,
    options = null,
    method = null
  ) => {
    const url = generateUrl({
      entries: entries,
      slug: slug,
      username: username,
      options: options,
      method: method
    });
    return Vue.axios.get(url).catch(function(error) {
      throw new Error(`Api getJson ${error}`);
    });
  },
  postJson: (
    entries,
    formData,
    username = null,
    options = null,
    method = null,
    isApi = true
  ) => {
    const url = generateUrl({
      entries: entries,
      username: username,
      options: options,
      method: method,
      isApi: isApi
    });
    const csrftoken = Cookies.get("csrftoken");
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "application/json"
    };
    const data = formData;

    return Vue.axios
      .post(url, data, {
        headers: headers
      })
      .catch(function(error) {
        alert("エラーが発生しました。");
        // const formatedError = formatErrorResponse(error);
        // alert(formatedError);
        throw new Error(`Api postJson ${error}`);
      });
  },
  putJson: (entries, slug = null, formData, username = null, method = null) => {
    const url = generateUrl({
      entries: entries,
      slug: slug,
      username: username,
      method: method
    });
    const csrftoken = Cookies.get("csrftoken");
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "application/json"
    };
    const data = formData;

    return Vue.axios
      .put(url, data, { headers: headers })
      .catch(function(error) {
        alert("エラーが発生しました。");
        throw new Error(`Api putJson${error}`);
      });
  },

  patchJson: (entries, slug, formObj, username = null) => {
    const url = generateUrl({
      entries: entries,
      slug: slug,
      username: username
    });
    const csrftoken = Cookies.get("csrftoken");
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "application/json"
    };
    const data = formObj;

    return Vue.axios
      .patch(url, data, { headers: headers })
      .catch(error => {
        alert("エラーが発生しました。");
        throw new Error(`Api patchJson${error}`);
      });
  },
  normalGetJson(url) {
    const headers = {
      "Content-Type": "application/json"
    };
    return Vue.axios
      .get(url, { headers: headers })
      .catch(error => {
        alert("エラーが発生しました。");
        throw new Error(`Api normalGetJson${error}`);
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
      checkFormObj.errors = [];
    })
    .catch(function(error) {
      checkFormObj.errors = error.response.data[formName];
    });
};

const beforeDebounceGetJson = (
  entries,
  receiveObj,
  key,
  slug = null,
  username = null,
  options = null,
  method = null
) => {
  Api.getJson(
    entries,
    (slug = slug),
    (username = username),
    (options = options),
    (method = method)
  ).then(response => {
    receiveObj[key] = response.data.results;
    if (!(receiveObj.next === undefined)) {
      receiveObj.next = response.data.next;
    }
  });
};

export { Api };
export const debouncedCheckOneForm = _.debounce(checkOneForm, 1000);
export const debounceGetJson = _.debounce(beforeDebounceGetJson, 1000);
