import store from '@/store'

import { Module, VuexModule, Mutation, Action, getModule } from 'vuex-module-decorators'
import axios from 'axios'
import { ArticleInfo, SiteInfo } from '@/dto'


@Module({ dynamic: true, store, name: "article", namespaced: true })
export class ArticleStore extends VuexModule {
    articles: ArticleInfo[] = []
    sites: { [key: number]: SiteInfo } = {};

    @Mutation
    setData(articles: ArticleInfo[], sites: {
        [key: number]: SiteInfo
    }) {
        this.articles = articles;
        this.sites = sites;
    }

    get soterdAtricles(): ArticleInfo[] {
        return this.articles.sort((prev, next) => {
            return next.updatedDate.getTime() - prev.updatedDate.getTime();
        });
    }

    @Action({ rawError: true })
    async updateList() {
        const response = await axios.get(`rss`);

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

        this.setData(articles, localSites);
    }
}

export const articleModule = getModule(ArticleStore)