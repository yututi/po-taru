import store from '@/store'

import { Module, VuexModule, Mutation, Action, getModule } from 'vuex-module-decorators'
import axios from 'axios'

@Module({ dynamic: true, store, name: "auth", namespaced: true })
export default class Auth extends VuexModule {
    isAuthenticated: boolean = false;

    @Mutation
    setAuth(isAuthenticated: boolean) {
        this.isAuthenticated = isAuthenticated;
    }

    @Action
    async login(id: string, password: string) {
        if(process.env.NODE_ENV == 'development'){
            this.setAuth(true);
            return true
        }
        var resposne = await axios.post('login', {
            id: id,
            password: password
        });
        if (resposne.status >= 200 && resposne.status < 300) {
            // 2XXなら認証成功
            this.setAuth(true);
        }
        return this.isAuthenticated;
    }
}

export const authModule = getModule(Auth)