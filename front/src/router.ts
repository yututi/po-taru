import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
            meta: { requireAuth: true },
            children: [
                {
                    path: '/rss',
                    name: 'rss',
                    component: () => import('./views/home/RSSReader.vue')
                },
                {
                    path: '/memo',
                    name: 'memo',
                    component: () => import('./views/home/MemoPage.vue')
                },
                {
                    path: '/',
                    name: 'landing',
                    component: () => import('./views/home/Landing.vue')
                }
            ]
        },
        {
            path: '/login',
            name: 'login',
            component: () => import(/* webpackChunkName: "about" */ './views/Login.vue'),
            meta: { requireAuth: false }
        }
    ]
})

export default router;