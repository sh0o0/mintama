import { Api } from "@/asynchronous/api";

export default {
  apiGetMyself(context) {
    context.commit("fetchStart");
    return Api.getJson('own', 'user')
      .then(response => {
        context.commit("setMyself", response.data);
        context.commit("fetchEnd");
      })
      .catch(error => {

      });
  },
  apiPutMyself(context, username) {
    context.commit("fetchStart");
    return Api.put("users", username, context.state.myself)
      .then(response => {
        context.commit("fetchEnd");
      })
      .catch(error => {
        throw new Error(`actions put: ${error}`)
      });
  },
  apiPatchMyself(context, {username, formObj}) {
    context.commit("fetchStart");
    return Api.patch("users", username, formObj)
      .then(response => {
        context.commit("fetchEnd");
      })
      .catch(error => {
        throw new Error(`actions patch: ${error}`)
      });
  },
};
