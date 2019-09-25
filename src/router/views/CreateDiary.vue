<template>
  <div>
    <h1 class="font-weight-bold">日記作成</h1>
    <v-divider></v-divider>
    <main>
      <v-text-field
        v-model="formObj.diary.title"
        background-color="amber"
        solo
        autofocus
        label="タイトル：未入力の場合、日付が自動で入ります。"
        class="pa-2 font-weight-bold"
      />
      <v-card
        v-for="(section, index) in formObj.diary.sections"
        :key="index"
        class="mb-1 mx-2"
        flat
        outlined
        elevation="5"
      >
        <v-card-actions>
          <v-text-field background-color="amber" label="見出し" shaped solo v-model="section.heading" />
        </v-card-actions>
        <v-card-actions>
          <v-textarea outlined auto-grow label="内容" v-model="section.content"></v-textarea>
        </v-card-actions>
        <v-card-actions>
          <v-combobox
            v-model="section.categories"
            :items="categoryList"
            item-value="id"
            item-text="name"
            label="カテゴリー"
            multiple
            chips
          ></v-combobox>
        </v-card-actions>
        <v-card-actions>
          <v-combobox
            v-model="section.references"
            :items="referenceList"
            label="参考資料"
            multiple
            chips
          ></v-combobox>
        </v-card-actions>
      </v-card>
    </main>
    <v-btn link @click="addSection" class="orange darken-2 mb-10" fab dark fixed bottom right>
      <v-icon dark>mdi-plus</v-icon>
    </v-btn>
  </div>
</template>

<script>
import FormatHelper from "@/helper/format";
import { Api } from '@/asynchronous/api'

export default {
  data() {
    return {
      formObj: {
        diary: {
          title: this.formatedDate(new Date().toISOString().substr(0, 10)),
          sections: []
        }
      },
      categoryList: [],
      referenceList: []
    };
  },
  methods: {
    addSection() {
      const section = {
        heading: "",
        categories: [],
        content: "",
        references: []
      };
      this.formObj.diary.sections.push(section);
    },
    sectionCount() {
      return this.formObj.diary.sections.length();
    },
    formatedDate(date) {
      return FormatHelper.dateToJp(date);
    }
  },
  created() {
    this.addSection();
    const that = this;
    Api.get('accounts/api/category').then(response => {
      console.log(response.data.results)
      that.categoryList = response.data.results
    })
  }
};
</script>