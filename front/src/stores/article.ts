import store from '@/store'
import Vue from 'vue'

import { Module, VuexModule, Mutation, Action, getModule } from 'vuex-module-decorators'
import axios, { AxiosResponse } from 'axios'
import { ArticleInfo, SiteInfo } from '@/dto'

class InitPayload {
    constructor(public siteInfos: SiteInfo[],
        public articles: ArticleInfo[]) { }
}

class AddPayload {
    constructor(public articles: ArticleInfo[], public currentPage: number) { }
}

@Module({ dynamic: true, store, name: "article", namespaced: true })
export class ArticleStore extends VuexModule {
    articles: ArticleInfo[] = []
    sites: SiteInfo[] = [];
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
        this.sites = this.sites.filter(site => !ids.includes(site.id))
    }

    @Mutation
    clearPage() {
        this.page = 0
        this.articles = []
        this.sites = [];
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

        const localSites: SiteInfo[] = (response.data.rssInfos as Partial<SiteInfo>[]).map(info => {
            return new SiteInfo(info.id, info.site_name, info.url)
        });

        const siteMap = new Map<number, SiteInfo>()
        localSites.forEach(site => {
            siteMap.set(site.id, site)
        })

        const articles = response.data.articles.map((r: Partial<ArticleInfo>) => {
            return new ArticleInfo(
                r.site,
                siteMap.has(r.site) ? siteMap.get(r.site).site_name : '',
                r.date,
                r.description,
                r.link,
                r.img
            );
        });

        this.initPage(new InitPayload(localSites, articles))
    }

    get filteredIds() {
        return this.sites.filter(site => !site.isIgnoreRequired).map(site => site.id);
    }

    @Action({ rawError: true })
    async updateArticles() {

        const localSites = this.sites;
        const filteredIds = this.filteredIds

        if (filteredIds.length == 0) {
            return this.setArticles([]);
        }

        const response = await axios.get('article', {
            params: {
                page: 0,
                rssIds: filteredIds
            }
        });

        const siteMap = new Map<number, SiteInfo>()
        localSites.forEach(site => {
            siteMap.set(site.id, site)
        })

        const articles: ArticleInfo[] = response.data.articles.map((r: Partial<ArticleInfo>) => {
            return new ArticleInfo(
                r.site,
                siteMap.has(r.site) ? siteMap.get(r.site).site_name : '',
                r.date,
                r.description,
                r.link,
                r.img
            );
        });

        const sorted = this.displayArticles;
        const latest: Date = sorted.length > 0 ? sorted[0].updatedDate : new Date(0)
        const needsUpdate = articles.some(article => {
            return article.updatedDate.getTime() > latest.getTime()
        }) || filteredIds.length > 0;

        if (needsUpdate) this.setArticles(articles);
    }

    @Action({ rawError: true })
    async nextArticles() {
        const localSites = this.sites;
        const nextPage = this.page + 1;

        const response = await axios.get('article', {
            params: {
                page: nextPage,
                rssIds: this.filteredIds
            }
        });
        const siteMap = new Map<number, SiteInfo>()
        localSites.forEach(site => {
            siteMap.set(site.id, site)
        })

        const articles = response.data.articles.map((r: Partial<ArticleInfo>) => {
            return new ArticleInfo(
                r.site,
                siteMap.has(r.site) ? siteMap.get(r.site).site_name : '',
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