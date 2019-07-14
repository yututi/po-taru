<template>
  <div class="rss-reader">
    <div
      class="rss-reader__item rss-item"
      v-for="(rssInfos, title, index) in groupingRssInfo"
      :key="title"
    >
      <expansion-panel :id="index.toString()" :title="title">
        <template v-slot:body>
          <div class="rss-links">
            <a
              class="rss-links__item rss-link"
              target="_blank"
              v-for="(info, index) in rssInfos"
              :href="info.link"
              :key="title + index.toString()"
            >{{info.title}}</a>
          </div>
        </template>
      </expansion-panel>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import ExpansionPanel from "@/components/ExpansionPanel.vue";
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

@Component({
  components: {
    ExpansionPanel
  }
})
export default class RSSReader extends Vue {
  rssInfos: RssInfo[] = [];
  fetchedRssInfos: FetchedRssInfo[] = [];

  _domParser!: DOMParser;
  _cancelId!: number;
  _lastFetched!: Date;

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
      let isFetchedAny = false;
      axios.get(data.url).then(response => {
        const doc = this._domParser.parseFromString(response.data, "text/xml");
        const siteTitle = query4TextFromDoc(doc, "channel title");

        doc.querySelectorAll("item").forEach(item => {
          const dateVal = query4Text(item, "date");
          const updateDate = new Date(dateVal || 0);
          if (updateDate >= this._lastFetched) {
            const title = query4Text(item, "title");
            const link = query4Text(item, "link");
            const info = new FetchedRssInfo(
              data.id,
              siteTitle,
              updateDate,
              title,
              link
            );
            this.fetchedRssInfos.push(info);
            isFetchedAny = true;
          }
        });
        if (isFetchedAny) {
          const date = new Date();
          date.setSeconds(0);
          date.setMilliseconds(0);
          this._lastFetched = date;
        }
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
    this._lastFetched = new Date(0);
    this.updateList();
    this._cancelId = setInterval(() => {
      this.updateList();
    }, 60 * 1000);
  }
  beforeDestroy() {
    clearInterval(this._cancelId);
  }
}
</script>
<style lang="stylus">
@require '../styles/rss.styl';
</style>
