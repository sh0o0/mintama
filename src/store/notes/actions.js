import { Api } from "@/asynchronous/api";

export default {
  listOwnNote(context, username) {
    const url = `api/notes/?username=${username}`
    return Api.get(url)
      .then(response => {
        context.commit("setNotes", response.data);
      })
      .catch(error => {
        throw new Error(`listMyselfNote: ${error}`)
      });
  },
  retrieveNote(context, slug) {
    const url = `api/notes`
    return Api.get(url, slug)
      .then(response => {
        context.commit("setNote", response.data);
      })
      .catch(error => {
        throw new Error(`retrieveNote: ${error}`)
      });
  },
  createNote(context, formObj) {
    return Api.post("api/notes", formObj)
      .then(response => {
        //
      })
      .catch(error => {
        throw new Error(`createNote: ${error}`)
      });
  },
  partialUpdateNote(context, slug, formObj) {
    const url = `api/notes`
    return Api.patch("api/notes", slug, formObj)
      .then(response => {
        //
      })
      .catch(error => {
        throw new Error(`partialUpdateNote: ${error}`)
      });
  },
};
