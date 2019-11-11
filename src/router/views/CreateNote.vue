<template>
  <div>
    <h2 class="font-weight-bold">ノート作成</h2>
    <v-divider></v-divider>
    <main>
      <v-text-field
        v-model="formObj.title"
        background-color="amber"
        solo
        autofocus
        label="タイトル：未入力の場合、日付が自動で入ります。"
        class="pa-2 font-weight-bold"
      />
      <v-card
        v-for="(section, index) in formObj.sections"
        :key="index"
        class="mb-12 mx-2"
        flat
        outlined
        elevation="5"
      >
        <v-card-actions>
          <v-text-field
            background-color="grey lighten-1"
            label="見出し"
            solo
            v-model="section.heading"
            append-outer-icon="mdi-delete"
            @click:append-outer="deleteSection(index)"
          />
        </v-card-actions>
        <v-card-actions>
          <v-textarea outlined auto-grow label="内容" v-model="section.content"></v-textarea>
        </v-card-actions>
        <v-card-actions>
          <v-combobox
            v-model="section.categories_dict"
            :items="categoryList"
            label="カテゴリー"
            item-value="id"
            item-text="name"
            multiple
            chips
          ></v-combobox>
        </v-card-actions>
        <v-card-actions>
          <v-combobox
            v-model="section.references_dict"
            :items="referenceList"
            item-value="id"
            item-text="title"
            label="参考資料"
            multiple
            chips
          ></v-combobox>
        </v-card-actions>
      </v-card>
    </main>
    <v-row class="bottom-btns">
      <v-btn link @click="addSection" class="blue-grey lighten-2 mr-2" fab dark>
        <v-icon dark>mdi-plus</v-icon>
      </v-btn>
      <v-btn link @click="post" class="orange darken-2" fab dark>作成</v-btn>
    </v-row>

    <v-dialog v-model="dialog" @click="dialog = false" width="500">
      <v-card>
        <v-card-title class="headline">作成しました。Twitterに投稿しますか？</v-card-title>
          <form method="post" action="/socials/login/twitter/" ref="twitter" class="ma-2">
            <v-textarea name="content" v-model="twitterContent" />
          </form>
        <v-card-actions>
          <div class="flex-grow-1"></div>
          <template>
            <v-btn v-if="isLinkedTwitter" color="blue lighten-1" text @click="postTwitter()">する</v-btn>
            <v-btn v-else color="blue lighten-1" text @click="connectAndPostTwitter()">する / Twitter連携</v-btn>
          </template>
          <v-btn text @click="dialog = false">しない</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { dateToJapan } from "@/helper/format";
import { Api } from "@/asynchronous/api";
import moment from "moment";

export default {
  data() {
    return {
      formObj: {
        title: moment()
          .utc()
          .format("YYYY年MM月DD日"),
        sections: [
          {
            heading: "",
            content: "",
            categories_dict: [],
            references_dict: []
          }
        ]
      },
      categoryList: [],
      referenceList: [],
      dialog: false,
      twitterContent: "",
      isLinkedTwitter: false,
    };
  },
  computed: {
    ...mapGetters('accounts', ['getMyself']),
  },
  methods: {
    sectionCount() {
      try {
        var count = this.formObj.sections.length;
      } catch (e) {
        return 0;
      }
      return count;
    },
    isSectionEmpty(section) {
      if (section.heading !== "") return false;
      if (section.content !== "") return false;
      if (section.categories_dict.length !== 0) return false;
      if (section.heading_dict.length !== 0) return false;

      return true;
    },
    addSection() {
      const count = this.sectionCount();
      if (!(count === 0)) {
        const lastIndex = this.sectionCount() - 1;
        if (this.isSectionEmpty(this.formObj.sections[lastIndex])) return;
      }
      const section = {
        heading: "",
        content: "",
        categories_dict: [],
        references_dict: []
      };
      this.formObj.sections.push(section);
    },
    formatedDate(date) {
      return FormatHelper.dateToJapan(date);
    },

    post() {
      const that = this;
      if (this.validateFormObj()) {
        Api.postJson("notes", this.formObj)
          .then(response => {
            that.makeTwitterContent();
            that.checkLinkedTwitter();
            that.dialog = true;
            // that.$router.push({
            //   name: "personalNoteList",
            //   params: { username: this.$route.params.username }
            // });
          })
          .catch(error => {
            alert("作成に失敗しました。");
          });
      }
    },
    validateFormObj() {
      if (this.formObj.title === "") {
        this.formObj.title = moment()
          .utc()
          .format("YYYY年MM月DD日");
      }

      const sections = this.formObj.sections;
      for (let sectionIndex in sections) {
        let heading = sections[sectionIndex].heading;
        if (heading === "") {
          alert(
            `${Number(sectionIndex) +
              1}のセクションの見出しが空白です。入力してください。`
          );
          return false;
        }
      }
      return true;
    },
    deleteSection(index) {
      const count = this.sectionCount();
      if (count in [0, 1]) return;
      this.formObj.sections.splice(index, 1);
    },

    checkLinkedTwitter() {
      const oauths = this.getMyself['social_auth'];
      for (const oauth of oauths) {
        if (oauth['provider'] === 'twitter') {
          this.isLinkedTwitter = true;
          return;
        }
      }
      this.isLinkedTwitter = false;
    },

    makeTwitterContent() {
      let content = "今日の学習\n";
      for (const section of this.formObj.sections) {
        content += `\n■ ${section.heading}`;
      }
      this.twitterContent = content;
    },

    postTwitter() {
      this.makeTwitterContent();
      const username = this.$route.params.username;
      const data = {content: this.twitterContent}
      const self = this;
      Api.postJson("socials/twitter", data, null, null, null, false)
        .then(res => {
          alert('投稿しました')
        })
        .catch(error => {
          alert("投稿に失敗しました");
        })
        .finally(() => {
          self.dialog = false;
          self.$router.push({name: 'home'})
        });
    },
    connectAndPostTwitter() {
      this.$refs.twitter.submit();
      alert('投稿しました');
    }
  },
  created() {
    const that = this;
    Api.getJson("categories").then(response => {
      that.categoryList = response.data.results;
    });
    Api.getJson("references", null, this.$route.params.username).then(
      response => (that.referenceList = response.data.results)
    );
  }
};
</script>