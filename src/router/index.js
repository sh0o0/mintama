import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home'
import Profile from './views/Profile'
import EntryProfile from './views/EntryProfile'
import MyPortfolios from './views/MyPortfolios'
import MyReferences from './views/MyReferences'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
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
  ]
})