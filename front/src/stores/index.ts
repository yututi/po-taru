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

    @Action({ rawError: true })
    async login({ id, password }: { id: string, password: string }) {
        // if(process.env.NODE_ENV == 'development'){
        //     this.setAuth(true);
        //     return true
        // }
        console.log(id)
        console.log(password)
        var resposne = await axios.post('login', {
            username: id,
            password: password
        });
        console.log(resposne.headers)
        if (resposne.status >= 200 && resposne.status < 300) {
            // 2XXなら認証成功
            console.log(resposne.headers)
            this.setAuth(true);
        }
        return this.isAuthenticated;
    }
}

export const authModule = getModule(Auth)