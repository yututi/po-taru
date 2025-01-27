import store from '@/store'
import Vue from 'vue'

import { Module, VuexModule, Mutation, Action, getModule } from 'vuex-module-decorators'
import axios, { AxiosResponse } from 'axios'

@Module({ dynamic: true, store, name: "global", namespaced: true })
export class GlobalStore extends VuexModule {
    isLoading: boolean = false;
    // infoMessages: string[] = []
    // errorMessages: string[] = []

    @Mutation
    setIsLoading(isLoading: boolean) {
        this.isLoading = isLoading
    }

    // @Mutation
    // setInfoMessage(message: string) {
    //     this.infoMessages.push(message)
    // }

    // @Mutation
    // removeInfoMessage(message: string) {
    //     this.infoMessages = this.infoMessages.filter(msg => msg !== message)
    // }

    // @Mutation
    // setErrrorMessage(message: string) {
    //     this.errorMessages.push(message)
    // }
    // @Mutation
    // removeErrorMessage(message: string) {
    //     this.errorMessages = this.errorMessages.filter(msg => msg === message)
    // }


    @Action({ rawError: true })
    pushInfoMessage(message: string) {
        Vue.$poppuappu.show(message)
    }
    @Action({ rawError: true })
    pushErrorMessage(message: string) {
        Vue.$poppuappu.show(message)
    }
}

export const globalModule = getModule(GlobalStore)

