import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
// import './registerServiceWorker'
import axios from 'axios'
import { getCSRFToken } from './utlis'

if (process.env.NODE_ENV === "production") {
    axios.defaults.baseURL = "api"
    Vue.config.productionTip = false
    axios.interceptors.request.use(request => {

        if (request.headers) {
            request.headers['X-CSRFToken'] = getCSRFToken()
        }
    
        return request
    })    
} else {
    axios.defaults.baseURL = "http://localhost:8000/api"
}


axios.interceptors.response.use(response => {
    if (response.status == 401) {
        router.push("/login") // TODO 未検証
    }
    return response;
})

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
