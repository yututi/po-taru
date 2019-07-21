import store from '@/store'
import Vue from 'vue'

import { Module, VuexModule, Mutation, Action, getModule } from 'vuex-module-decorators'
import axios, { AxiosResponse } from 'axios'
import { ArticleInfo, SiteInfo } from '@/dto'

class InitPayload {
    constructor(public siteInfos: { [key: number]: SiteInfo },
        public articles: ArticleInfo[]) { }
}

class AddPayload {
    constructor(public articles: ArticleInfo[], public currentPage: number) { }
}

@Module({ dynamic: true, store, name: "article", namespaced: true })
export class ArticleStore extends VuexModule {
    articles: ArticleInfo[] = []
    sites: { [key: number]: SiteInfo } = {};
    page: number = 0;

    @Mutation
    initPage(payload: InitPayload) {
        this.sites = payload.siteInfos;
        this.articles = payload.articles;
    }

    @Mutation
    addPage(payload: AddPayload) {
        this.articles = payload.articles.concat(this.articles)
        this.page = payload.currentPage;
    }

    @Mutation
    setArticles(articles: ArticleInfo[]) {
        this.articles = articles;
    }

    @Mutation
    addSiteInfo(site: SiteInfo) {
        Vue.set(this.sites, site.id, site)
    }

    @Mutation
    removeSiteInfo(ids: number[]) {
        ids.forEach(id => {
            Vue.delete(this.sites, id)
        })
    }

    @Mutation
    clearPage() {
        this.page = 0
        this.articles = []
        this.sites = {}
    }

    get displayArticles(): ArticleInfo[] {
        return this.articles.sort((prev, next) => {
            return next.updatedDate.getTime() - prev.updatedDate.getTime();
        });
    }

    get displaySites() {
        return this.sites;
    }

    @Action({ rawError: true })
    async initArticles() {

        this.clearPage()

        const response = await axios.get('article', {
            params: {
                page: this.page
            }
        });

        const localSites = response.data.rssInfos.reduce(
            (sites: { [key: number]: SiteInfo }, site: Partial<SiteInfo>) => {
                sites[site.id] = new SiteInfo(site.id, site.site_name, site.url);
                return sites;
            },
            {}
        );

        const articles = response.data.articles.map((r: Partial<ArticleInfo>) => {
            return new ArticleInfo(
                r.site,
                localSites[r.site] ? localSites[r.site].site_name : '',
                r.date,
                r.description,
                r.link,
                r.img
            );
        });

        this.initPage(new InitPayload(localSites, articles))
    }
    @Action({ rawError: true })
    async updateArticles() {

        const localSites = this.sites;

        const response = await axios.get('article', {
            params: {
                page: 0,
                rssIds: Object.keys(localSites)
            }
        });

        const articles: ArticleInfo[] = response.data.articles.map((r: Partial<ArticleInfo>) => {
            return new ArticleInfo(
                r.site,
                localSites[r.site] ? localSites[r.site].site_name : '',
                r.date,
                r.description,
                r.link,
                r.img
            );
        });

        const sorted = this.displayArticles;
        const latest: Date = sorted ? sorted[0].updatedDate : new Date(0)
        const needsUpdate = articles.some(article => {
            return article.updatedDate.getTime() > latest.getTime()
        });

        if (needsUpdate) this.setArticles(articles);
    }

    @Action({ rawError: true })
    async nextArticles() {
        const localSites = this.sites;
        const nextPage = this.page + 1;

        const response = await axios.get('article', {
            params: {
                page: nextPage,
                rssIds: Object.keys(localSites)
            }
        });

        const articles = response.data.articles.map((r: Partial<ArticleInfo>) => {
            return new ArticleInfo(
                r.site,
                localSites[r.site] ? localSites[r.site].site_name : '',
                r.date,
                r.description,
                r.link,
                r.img
            );
        });

        this.addPage(new AddPayload(articles, nextPage))
    }


    @Action({ rawError: true })
    async submitNewSiteInfo(url: string): Promise<SiteInfo> {
        const response: AxiosResponse<SiteInfo> = await axios.post('rss', {
            url: url
        })
        const data = response.data;
        const site = new SiteInfo(data.id, data.site_name, data.url)
        this.addSiteInfo(site)
        return Promise.resolve(site)
    }

    @Action({ rawError: true })
    async deleteSiteInfo(ids: number[]) {
        await axios.delete('rss', {
            data: { rssIds: ids }
        })
        this.removeSiteInfo(ids)
        this.initArticles();
    }
}

export const articleModule = getModule(ArticleStore)