import Vue from 'vue'
import Router from 'vue-router'

import Home from './views/Home'

import Profile from './views/Profile'
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
      component: Home,
    },
    //list
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
    //personal list
    {
      path: '/:username',
      name: 'profile',
      component: Profile,
    },
    {
      path: '/:username/notes',
      name: 'personalNoteList',
      component: NoteList,
    },
    {
      path: '/:username/references',
      name: 'personalReferenceList',
      component: ReferenceList,
    },
    {
      path: '/:username/boards',
      name: 'boardList',
      component: BoardList,
    },
    //specific
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
    //create
    {
      path: '/notes/create',
      name: 'createNote',
      component: CreateNote,
    },
    //update
    {
      path: '/settings/profiles',
      name: 'settingsProfile',
      component: UpdateProfile,
    },
    {
      path: '/:username/notes/:noteId/update',
      name: 'updateNote',
      component: UpdateNote,
    },
  ]
})