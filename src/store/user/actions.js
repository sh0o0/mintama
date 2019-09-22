import { Rest } from "@/asynchronous/api";

export default {
  apiGetMyself(context) {
    context.commit("fetchStart");
    return Rest.get("account/api/user", "my!own!info")
      .then(response => {
        context.commit("setMyself", response.data);
        context.commit("fetchEnd");
      })
      .catch(error => {

      });
  },
  apiPutMyself(context) {
    context.commit("fetchStart");
    return Rest.put("account/api/user", "my!own!info", context.state.myself)
      .then(response => {
        context.commit("fetchEnd");
      })
      .catch(error => {
        throw new Error(`actions put: ${error}`)
      });
  },
  apiPatchMyself(context, formObj) {
    context.commit("fetchStart");
    return Rest.patch("account/api/user", "my!own!info", formObj)
      .then(response => {
        context.commit("fetchEnd");
      })
      .catch(error => {
        throw new Error(`actions patch: ${error}`)
      });
  },
};
