import store from '@/store'
import { Module, VuexModule, Mutation, Action, getModule } from 'vuex-module-decorators'
import axios from 'axios'

export class AuthInfo {
    constructor(public id: string, username: string) { }
}

@Module({ dynamic: true, store, name: "auth", namespaced: true })
export class Auth extends VuexModule {
    authInfo: AuthInfo = new AuthInfo("", "");

    get isAuthenticated() {
        return !!this.authInfo.id;
    }

    @Mutation
    setAuthInfo(authInfo: AuthInfo) {
        this.authInfo = authInfo;
    }

    @Action({ rawError: true })
    async login({ id, password }: { id: string, password: string }) {

        var response = await axios.post('login', {
            username: id,
            password: password
        });

        this.setAuthInfo(new AuthInfo(response.data.id, response.data.username));
    }

    @Action({ rawError: true })
    async logout() {
        await axios.post('logout')
        this.setAuthInfo(new AuthInfo("", ""));
    }

    @Action({ rawError: true })
    async getUserInfo() {
        var response = await axios.get('auth/me');
        this.setAuthInfo(new AuthInfo(response.data.id, response.data.username));
    }
}

export const authModule = getModule(Auth)
