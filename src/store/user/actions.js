import Api from '@/asynchronous/api'

export default {
  apiGetMyself(context) {
    context.commit('fetchStart')
    return Api
      .get('api', 'user/my!own!info')
      .then(response => {
        console.log('status:', response.status);
        console.log('data', response.data);
        context.commit('setMyself', response.data);
        context.commit('fetchEnd');
      })
      .catch((response) => {
        context.commit('setError', response.errors)
      })
  },
  apiPutMyself(context) {
    context.commit('fetchStart')
    return Api
    .put('api', 'user/my!own!info', context.state.myself) 
    .then(response => {
      console.log(response.status)
      context.commit('fetchEnd')
    })
    .catch((response) => {
      context.commit('setError', response.errors)
    })
  }
}
