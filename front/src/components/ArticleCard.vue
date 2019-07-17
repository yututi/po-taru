<template>
  <div class="article-card" @click="open">
    <div class="article-card__thumbnail thumbnail">
      <div class="thumbnail__title">{{siteName}}</div>
      <img class="thumbnail__img" v-if="img" :src="img" alt="thumbnail" />
    </div>
    <div class="article-card__content article-content">
      <a class="article-content__link" :href="link">{{description}}</a>
      <div class="article-content__updated">{{updatedTime}}</div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import { ArticleInfo } from "@/dto";

@Component
export default class ArticleCard extends Vue {
  @Prop({ type: ArticleInfo, required: true })
  article!: ArticleInfo;

  _open: Function;

  get siteName() {
    return this.article.siteName;
  }

  get img() {
    return this.article.img;
  }

  get description() {
    return this.article.description;
  }

  get link() {
    return this.article.link;
  }

  get updatedTime() {
    const date = this.article.updatedDate;
    return `${date.getFullYear()}年${date.getMonth() +
      1}月${date.getDate()}日${date.getHours()}時`;
  }

  open() {
    this._open();
  }
  mounted() {
    this._open = () => {
      window.open(this.link);
    };
  }
}
</script>
<style lang="stylus">
@require '../styles/palette.styl';

.article-card {
  display: flex;
  border: 1px solid gainsboro;
  padding: 5px;
  box-shadow: 0 0 0 0 gainsboro;
  transition: box-shadow 0.3s;

  &__thumbnail {
  }

  &__content {
    padding: 5px 10px;
  }

  &:hover {
    box-shadow: 0 0 8px 1px gainsboro;

    .thumbnail {
      &__title {
        opacity: 1;
        width: 100%;
      }
    }
  }
}

.article-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;

  &__link {
    flex: 1;
    text-align: left;
    text-decoration: none;
  }
}

.thumbnail {
  position: relative;

  &__title {
    position: absolute;
    background-color: rgba(50, 150, 220, 0.5);
    color: $primaryText;
    padding: 0.3em;
    box-sizing: border-box;
    height: 100%;
    width: 0px;
    opacity: 0;
    transition: opacity 0.3s, width 0.3s;
    white-space: nowrap;
  }

  &__img {
    width: 100px;
    height: 100px;
    object-fit: cover;
  }
}
</style>
