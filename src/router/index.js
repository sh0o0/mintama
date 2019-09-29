import Vue from 'vue'
import Router from 'vue-router'

import CreateNote from './views/CreateNote'
import UpdateProfile from './views/UpdateProfile'
import UpdateNote from './views/UpdateNote'
import Home from './views/Home'
import Note from './views/Note'
import NoteList from './views/NoteList'
import PortfolioList from './views/PortfolioList'
import Profile from './views/Profile'
import ReferenceList from './views/ReferenceList'


Vue.use(Router)

export default new Router({
  routes: [
    //home
    {
      path: '/',
      name: 'home',
      component: Home
    },
    //settings
    // {
    //   path: '/settings',
    //   name: 'settings',
    //   component: Settings,
    // },
    {
      path: '/settings/profiles',
      name: 'settingsProfile',
      component: UpdateProfile,
    },
    // {
    //   path: '/settings/password',
    //   name: 'settingsPassword',
    //   component: SettingsPassword,
    // },
    //app list
    {
      path: '/portfolios',
      name: 'portfolioList',
      component: PortfolioList,
    },
    {
      path: '/references',
      name: 'referenceList',
      component: ReferenceList,
    },
    {
      path: '/notes',
      name: 'noteList',
      component: NoteList,
    },
    // {
    //   path: '/todos',
    //   name: 'todoList',
    //   component: TodoList,
    // },
    //personal app list
    {
      path: '/:username',
      name: 'profile',
      component: Profile,
    },
    // {
    //   path: '/:username/portfolios',
    //   name: 'personalPortfolioList',
    //   component: PersonalPortfolioList,
    // },
    // {
    //   path: '/:username/references',
    //   name: 'personalReferenceList',
    //   component: PersonalReferenceList,
    // },
    {
      path: '/:username/notes',
      name: 'personalNoteList',
      component: NoteList,
    },
    //app info
    // {
    //   path: '/:username/portfolios/:portfolioId',
    //   name: 'portfolio',
    //   component: Portfolio,
    // },
    // {
    //   path: '/:username/references/:referenceId',
    //   name: 'reference',
    //   component: Reference,
    // },
    {
      path: '/:username/notes/:noteId',
      name: 'note',
      component: Note,
    },
    //app create
    // {
    //   path: '/portfolio/create',
    //   name: 'createPortfolio',
    //   component: CreatePortfolio,
    // },
    // {
    //   path: '/reference/create',
    //   name: 'createReference',
    //   component: CreateReference,
    // },
    {
      path: '/notes/create',
      name: 'createNote',
      component: CreateNote,
    },
    //app update
    // {
    //   path: '/:username/portfolios/:portfolioId/update',
    //   name: 'updatePortfolio',
    //   component: UpdatePortfolio,
    // },
    // {
    //   path: '/:username/references/:referenceId/update',
    //   name: 'updateReference',
    //   component: UpdateReference,
    // },
    {
      path: '/:username/notes/:noteId/update',
      name: 'updateNote',
      component: UpdateNote,
    },
  ]
})