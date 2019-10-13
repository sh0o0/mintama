<template>
  <div>
    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="gray" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>

    <h2 class="font-weight-bold">ノート編集</h2>
    <v-divider></v-divider>
    <main>
      <v-text-field
        v-model="formObj.title"
        background-color="amber"
        solo
        autofocus
        label="タイトル：未入力の場合、日付が自動で入ります。"
        class="pa-2 font-weight-bold"
        append-outer-icon="mdi-delete-forever"
        @click:append-outer="confirmDialog = true"
          
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
      <v-btn link @click="update" class="orange darken-2" fab dark>変更</v-btn>
    </v-row>
    
    <v-dialog v-model="updateDialog" @click="updateDialog = false" width="300">
      <v-card>
        <v-card-title class="headline">作成しました。</v-card-title>
        <v-card-actions>
          <div class="flex-grow-1"></div>
          <v-btn color="amber darken-1" text @click="updateDialog = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="confirmDialog" @click="confirmDialog = false" width="300">
      <v-card>
        <v-card-title class="headline">本当に削除しますか？</v-card-title>
        <v-card-actions>
          <div class="flex-grow-1"></div>
          <v-btn color="gray darken-1" text @click="deleteNote">する</v-btn>
          <v-btn color="gray darken-1" text @click="confirmDialog = false">しない</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deletedDialog" @click="deletedDialog = false" width="300">
      <v-card>
        <v-card-title class="headline">削除が完了しました。</v-card-title>
        <v-card-actions>
          <div class="flex-grow-1"></div>
          <router-link tag="div" :to="{name: 'personalNoteList', params: {username: $route.params.username}}">
            <v-btn link color="gray darken-1" text @click="deletedDialog = false">ノート一覧に移動する。</v-btn>
          </router-link>
        </v-card-actions>
      </v-card>
    </v-dialog>
    

  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { dateToJapan } from "@/helper/format";
import { Api } from "@/asynchronous/api";
import moment from "moment";

export default {
  data() {
    return {
      formObj: {},
      categoryList: [],
      referenceList: [],
      isLoading: false,
      updateDialog: false,
      confirmDialog: false,
      deletedDialog: false,
    };
  },
  computed: {
    ...mapGetters('accounts', ['getMyself'])
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
      if (section.categories.length !== 0) return false;
      if (section.heading.length !== 0) return false;

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
        categories: [],
        references: []
      };
      this.formObj.sections.push(section);
    },
    formatedDate(date) {
      return FormatHelper.dateToJapan(date);
    },

    update() {
      const that = this;
      if (this.validateFormObj()) {
        const username = this.$route.params.username;
        const noteId = this.$route.params.noteId;
        Api.putJson("notes", noteId, this.formObj, username)
          .then(response => {
            that.updateDialog = true;
          })
          .catch(error => {
            alert('変更に失敗しました。');
            console.log(error.response);
          });
      }
    },
    validateFormObj() {
      if (this.formObj.title === "") {
        this.formObj.title ===
          moment()
            .utf()
            .format("YYYY年MM月DD日");
      }

      const sections = this.formObj.sections;
      for (let sectionIndex in sections) {
        let heading = sections[sectionIndex].heading;
        if (heading === "") {
          alert(
            `${Number(sectionIndex) +1}
            のセクションの見出しが空白です。入力してください。`
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
    deleteNote() {
      const that = this;
      const noteId = this.$route.params.noteId;
      const username = this.$route.params.username
      Api.delete('notes', noteId, username).then(response => {
        that.deletedDialog = true
      }).catch(error => {
        alert('ノートの削除に失敗しました。')
      })
    }
  },
  created() {
    this.isLoading = true;
    const that = this;

    const noteId = this.$route.params.noteId;
    const username = this.$route.params.username;

    if (username !== this.getMyself.username) {
      this.$router.push({name: 'note', params: {username: username, noteId: noteId}})
      that.isLoading = false;
      return
    }

    Api.getJson("notes", noteId, username).then(response => {
      that.formObj = response.data;
      that.isLoading = false;
    }).catch(error => {
      that.isLoading = false;
      alert('このノートは存在しません。')
    });
    Api.getJson("categories").then(response => {
      that.categoryList = response.data.results;
    });
  }
};
</script>