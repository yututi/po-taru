export class ArticleInfo {
    constructor(
        public rssId: string,
        public siteName: string,
        public updated: string,
        public title: string,
        public link: string,
        public img: string
    ) {
        this.updatedDate = new Date(updated)
    }
    public updatedDate: Date;
}