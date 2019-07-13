import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
// import './registerServiceWorker'
import axios from 'axios'
import { getCSRFToken, isAuthErrorStatusCode } from './utlis'

Vue.config.productionTip = true

if (process.env.NODE_ENV === "production") {
    axios.defaults.baseURL = "api"
    axios.interceptors.request.use(request => {

        if (request.headers) {
            request.headers['X-CSRFToken'] = getCSRFToken()
        }

        return request
    })

    axios.interceptors.response.use(response => response, error => {
        const response = error.response;
        if (isAuthErrorStatusCode(response.status)) {
            if (router.currentRoute.path != "/login") {
                router.push({ path: "login", query: { redirect: router.currentRoute.path } })
            }
        }
    })
} else {
    axios.defaults.baseURL = "http://localhost:8000/api"
}

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
