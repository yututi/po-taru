import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import { authModule } from '@/stores/auth'

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

let isFirstRouting = true
router.beforeEach((to, from, next) => {
    if (to.meta.requireAuth !== false) {
        if (authModule.isAuthenticated) {
            return next()
        }

        // prevent route until authentication
        if (isFirstRouting) {
            isFirstRouting = false
            authModule.getUserInfo().then(() => {
                next();
            }).catch(() => {
                next('/login')
            })
            return
        }
        return next('/login')
    }
    return next()
})

export default router;