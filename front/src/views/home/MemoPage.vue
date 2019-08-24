<template>
  <div class="memo form">
    <div class="memo-holder form__item">
      <stretch-txt-area class="memo-holder__memo new-memo" v-model="newMemo.text"></stretch-txt-area>
    </div>
    <div class="form__action">
      <button
        class="button"
        :disabled="!newMemo.canSave"
        :class="{'button--disable':!newMemo.canSave}"
        v-rippuru
        @click="create(newMemo)"
      >保存</button>
    </div>
    <div class="form__item memo-holder" v-for="memo in sortedMemoList" :key="memo.id">
      <stretch-txt-area :editable="memo.isEditable" class="memo-holder__memo" v-model="memo.text"></stretch-txt-area>
      <div class="memo-holder__icons memo-icons">
        <div v-rippuru class="memo-icons__icon app-icon" @click="editOrUpdate(memo)">
          <i v-if="!memo.isEditable" class="fas fa-pen"></i>
          <i v-else class="fas fa-file-upload"></i>
        </div>
        <div v-rippuru class="memo-icons__icon app-icon" @click="deleteMemo(memo)">
          <i class="fas fa-trash-alt"></i>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import axios, { AxiosResponse } from "axios";
import StretchTxtArea from "@/components/StretchTxtArea.vue";
class MemoData {
  constructor(
    public id: number,
    public text: string,
    public last_updated: Date
  ) {
    this.oldText = text;
    this.updated = new Date(last_updated);
  }
  public oldText: string;
  public isEditable = false;
  public updated: Date;
  get isChanged() {
    return this.text != this.oldText;
  }
}
class NewMemoData {
  text: string = "";
  get canSave() {
    return !!this.text;
  }
}
@Component({
  components: {
    StretchTxtArea,
    ProgressCircle: () => import("@/components/ProgressCircle.vue")
  }
})
export default class Memo extends Vue {
  newMemo: NewMemoData = new NewMemoData();
  memoList: MemoData[] = [];

  get sortedMemoList() {
    return this.memoList.sort(
      (a, b) => b.updated.getTime() - a.updated.getTime()
    );
  }

  async create(memo: NewMemoData) {
    const response: AxiosResponse<Partial<MemoData>> = await axios.post(
      "memo/",
      {
        text: memo.text
      }
    );

    // blurしないと更新できない
    const textarea = this.$el.querySelector(".new-memo") as HTMLElement;
    textarea.blur();
    memo.text = "";

    const data = response.data;
    this.memoList.push(new MemoData(data.id, data.text, data.last_updated));
  }

  async editOrUpdate(memo: MemoData) {
    if (memo.isEditable && memo.isChanged) {
      await axios.patch(`memo/${memo.id}/`, {
        text: memo.text
      });
    }

    memo.isEditable = !memo.isEditable;
  }

  async deleteMemo(memo: MemoData) {
    await axios.delete(`memo/${memo.id}/`);
    this.memoList = this.memoList.filter(m => m.id != memo.id);
  }

  async mounted() {
    const response: AxiosResponse<Partial<MemoData>[]> = await axios.get(
      "memo/"
    );
    const found = response.data.map(
      data => new MemoData(data.id, data.text, data.last_updated)
    );

    this.memoList = found;
  }
}
</script>
<style lang="stylus">
@require '../../styles/palette.styl';

.memo {
  text-align: center;
  overflow: hidden;
}

.memo-holder {
  box-sizing: border-box;
  margin-top: 1em;
  margin-left: 1em;
  margin-right: 1em;
  position: relative;

  &__memo {
    width: 100%;
    padding: 12px;
  }

  &__icons {
    position: absolute;
    right: 5px;
    bottom: 5px;
  }
}

.memo-icons {
  display: flex;
  align-items: center;

  &__icon {
    cursor: pointer;
    border-radius: 50%;
    border: 1px solid gainsboro;
    box-sizing: border-box;
    background-color: white;
    width: 2em;
    height: 2em;

    & + & {
      margin-left: 5px;
    }
  }
}
</style>
