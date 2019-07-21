export class ArticleInfo {
    constructor(
        public site: number,
        public siteName: string,
        public date: string,
        public description: string,
        public link: string,
        public img: string
    ) {
        this.updatedDate = new Date(date)
    }
    public updatedDate: Date;
}

export class SiteInfo {
    constructor(public id: number, public site_name: string, public url: string) { }
    public isDeleteRequired: boolean = false;
}