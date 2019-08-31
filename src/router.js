import Vue from 'vue'
import Router from 'vue-router'

import Button from '@/components/Button.vue'
import List from '@/components/List.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'button',
      component: Button
    },
    {
      path: '/list',
      name: 'list',
      component: List,
    }
  ]
})