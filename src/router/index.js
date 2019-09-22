import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home'
import Account from './views/Account'
import EntryProfile from './views/EntryProfile'
import MyPortfolios from './views/MyPortfolios'
import MyReferences from './views/MyReferences'
import DiaryWrite from './views/DiaryWrite'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/account',
      name: 'account',
      component: Account,
    },
    {
      path: '/entry-profile',
      name: 'entryProfile',
      component: EntryProfile,
    },
    {
      path: '/portfolios',
      name: 'myPortfolios',
      component: MyPortfolios,
    },
    {
      path: '/references',
      name: 'myReferences',
      component: MyReferences,
    },
    {
      path: '/diaies/wirte',
      name: 'diaryWrite',
      component: DiaryWrite,
    },
  ]
})