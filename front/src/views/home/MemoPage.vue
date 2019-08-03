<template>
  <div class="memo form">
    <div class="memo-holder form__item" v-for="(memo, index) in memoList" :key="index">
      <textarea cols="30" rows="10" v-model="memo.text" @input="memo.isChanged=true"></textarea>
      <div class="actions">
        <div class="loader"></div>
        <button class="button" @click="save(memo)">保存</button>
      </div>
    </div>
    <div class="form__item"></div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios, { AxiosResponse } from "axios";

class MemoData {
  constructor(
    public id: number,
    public text: string,
    public last_updated: Date,
    public disp_no: number
  ) {}
  public isNewMemo: boolean = false;
  public isDispNoChanged: boolean = false;
}
@Component
export default class Memo extends Vue {
  memoList: MemoData[] = [];

  async save() {
    axios.post("memo", {});
  }

  async mounted() {
    const response: AxiosResponse<Partial<MemoData>[]> = await axios.get(
      "memo"
    );
    this.memoList = response.data.map(
      r => new MemoData(r.id, r.text, r.last_updated, r.disp_no)
    );
  }
}
</script>
<style lang="stylus">
.memo {
  text-align: center;
  overflow: hidden;
}
</style>
