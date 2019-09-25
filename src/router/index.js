import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home'
import Account from './views/Account'
import EntryProfile from './views/EntryProfile'
import MyPortfolios from './views/MyPortfolios'
import MyReferences from './views/MyReferences'
import CreateDiary from './views/CreateDiary'

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
      path: '/create/diary',
      name: 'createDiary',
      component: CreateDiary,
    },
  ]
})

// const sample = [
//   //home
//   {
//     path: '/',
//     name: 'home',
//     component: Home
//   },
//   //settings
//   {
//     path: '/settings',
//     name: 'settings',
//     component: Settings,
//   },
//   {
//     path: '/settings/profile',
//     name: 'settingsProfile',
//     component: EditProfile,
//   },
//   {
//     path: '/settings/password',
//     name: 'settingsPassword',
//     component: SettingsPassword,
//   },
//   //app list
//   {
//     path: '/portfolios',
//     name: 'portfolioList',
//     component: PortfolioList,
//   },
//   {
//     path: '/references',
//     name: 'referenceList',
//     component: ReferenceList,
//   },
//   {
//     path: '/diaries',
//     name: 'diaryList',
//     component: DiaryList,
//   },
//   // {
//   //   path: '/todos',
//   //   name: 'todoList',
//   //   component: TodoList,
//   // },
//   //personal app list
//   {
//     path: '/:username',
//     name: 'personalProfile',
//     component: PersonalProfile,
//   },
//   {
//     path: '/:username/portfolios',
//     name: 'personalPortfolioList',
//     component: PersonalPortfolioList,
//   },
//   {
//     path: '/:username/references',
//     name: 'personalReferenceList',
//     component: PersonalReferenceList,
//   },
//   {
//     path: '/:username/diaries',
//     name: 'personalDiaryList',
//     component: PersonalDiaryList,
//   },
//   //app info
//   {
//     path: '/:username/portfolio/:portfolioId',
//     name: 'portfolio',
//     component: Portfolio,
//   },
//   {
//     path: '/:username/reference/:referenceId',
//     name: 'reference',
//     component: Reference,
//   },
//   {
//     path: '/:username/diary/:diaryId',
//     name: 'diary',
//     component: Diary,
//   },
//   //app create
//   {
//     path: '/portfolio/create',
//     name: 'createPortfolio',
//     component: CreatePortfolio,
//   },
//   {
//     path: '/reference/create',
//     name: 'createReference',
//     component: CreateReference,
//   },
//   {
//     path: '/diary/create',
//     name: 'createDiary',
//     component: CreateDiary,
//   },
//   //app update
//   {
//     path: '/:username/portfolio/:portfolioId/update',
//     name: 'updatePortfolio',
//     component: UpdatePortfolio,
//   },
//   {
//     path: '/:username/reference/:referenceId/update',
//     name: 'updateReference',
//     component: UpdateReference,
//   },
//   {
//     path: '/:username/diary/:diaryId/update',
//     name: 'updateDiary',
//     component: UpdateDiary,
//   },
// ]