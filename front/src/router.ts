import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import { authModule } from '@/stores'

Vue.use(Router)

const router = new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
            meta: { requireAuth: true }
        },
        {
            path: '/login',
            name: 'login',
            component: () => import(/* webpackChunkName: "about" */ './views/Login.vue'),
            meta: { requireAuth: false }
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requireAuth)) {
        if (!authModule.isAuthenticated) {
            return next({
                path: '/login',
                query: { redirect: to.fullPath }
            });
        }
        return next()
    }
    return next()
})

export default router;