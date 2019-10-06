import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home'

import Profile from './views/Profile'
import PortfolioList from './views/PortfolioList'
import UpdateProfile from './views/UpdateProfile'

import Note from './views/Note'
import NoteList from './views/NoteList'
import CreateNote from './views/CreateNote'
import UpdateNote from './views/UpdateNote'

import BoardList from './views/BoardList'
import Board from './views/Board'

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
    {
      path: '/:username/boards',
      name: 'boardList',
      component: BoardList,
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
    {
      path: '/:username/boards/:boardId',
      name: 'board',
      component: Board,
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