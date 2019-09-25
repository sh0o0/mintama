import { Api, API_MYSELF_URL } from "@/asynchronous/api";

export default {
  listMyselfDiary(context) {
    return Api.get("diaries/api/diary", API_MYSELF_URL)
      .then(response => {
        context.commit("setDiaries", response.data);
      })
      .catch(error => {
        throw new Error(`listMyselfDiary: ${error}`)
      });
  },
  retrieveDiary(context, slug) {
    return Api.get("diaries/api/diary", slug)
      .then(response => {
        context.commit("setDiary", response.data);
      })
      .catch(error => {
        throw new Error(`retrieveDiary: ${error}`)
      });
  },
  createDiary(context, formObj) {
    return Api.post("account/api/diary", formObj)
      .then(response => {
        //
      })
      .catch(error => {
        throw new Error(`createDiary: ${error}`)
      });
  },
  partialUpdateDiary(context, slug, formObj) {
    return Api.patch("account/api/diary", slug, formObj)
      .then(response => {
        //
      })
      .catch(error => {
        throw new Error(`partialUpdateDiary: ${error}`)
      });
  },
};
