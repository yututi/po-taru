import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
// import './registerServiceWorker'
import axios from 'axios'

if (process.env.NODE_ENV === "production") {
    axios.defaults.baseURL = "api"
    Vue.config.productionTip = false
} else {
    axios.defaults.baseURL = "http://localhost:8000/api"
}

axios.interceptors.request.use(request=>{

    if(request.headers){
        request.headers['X-CSRFToken'] = getCSRFToken()
    }

    return request
})

function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

axios.interceptors.response.use(response => {
    if(response.status == 401){
        router.push("/login") // TODO 未検証
    }
    return response;
})

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
