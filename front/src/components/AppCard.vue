<template>
  <div class="rss-reader">
    <div v-for="(rssInfos, title) in groupingRssInfo" :key="title">
      <div>{{title}}</div>
      <div v-for="(info, index) in rssInfos" :key="title + index.toString()">
        <a :href="info.link">{{info.title}}</a>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import { authModule } from "@/stores";
import { query4Text, query4TextFromDoc } from "@/utlis";
import axios from "axios";

class RssInfo {
  constructor(
    public id: string,
    public url: string,
    public lastUpdated: Date
  ) {}
}
class FetchedRssInfo {
  constructor(
    public rssId: string,
    public stiteTitle: string,
    public date: Date,
    public title: string | null,
    public link: string | null
  ) {}
}

@Component
export default class RSSReader extends Vue {
  rssInfos: RssInfo[] = [];
  fetchedRssInfos: FetchedRssInfo[] = [];

  _domParser!: DOMParser;

  async updateList() {
    // const response = await axios.get(`rss/${authModule.authInfo.id}`);
    // this.rssInfos = response.data;
    this.rssInfos = [
      {
        id: "1",
        url: "http://blog.esuteru.com/index.rdf",
        lastUpdated: new Date(0)
      }
    ];
    this.rssInfos.forEach(data => {
      axios.get(data.url).then(response => {
        const doc = this._domParser.parseFromString(response.data, "text/xml");
        const siteTitle = query4TextFromDoc(doc, "channel title");

        doc.querySelectorAll("item").forEach(item => {
          const dateVal = query4Text(item, "date");
          const title = query4Text(item, "title");

          const link = query4Text(item, "link");
          const updateDate = new Date(dateVal || 0);
          if (updateDate > data.lastUpdated) {
            const info = new FetchedRssInfo(
              data.id,
              siteTitle,
              updateDate,
              title,
              link
            );
            this.fetchedRssInfos.push(info);
          }
        });
      });
    });
  }
  get groupingRssInfo(): { [key: string]: FetchedRssInfo[] } {
    const map: { [key: string]: FetchedRssInfo[] } = {};

    this.fetchedRssInfos.forEach(info => {
      if (!map[info.stiteTitle]) {
        map[info.stiteTitle] = [];
      }
      map[info.stiteTitle].push(info);
    });

    return map;
  }
  created() {
    this._domParser = new DOMParser();
  }
  mounted() {
    this.updateList();
  }
}
</script>
<style lang="stylus"></style>
