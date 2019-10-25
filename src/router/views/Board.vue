<template>
  <div class="wrapper">
    <v-row class="my-1">
      <template>
      <input 
      v-show="isInputBoardName" 
      class="font-weight-bold ml-5 headline" 
      @blur="updateBoardName()"
      @keydown.enter="updateBoardName()"
      v-model="board.name" 
      ref="boardName">
      <h1 v-show="!(isInputBoardName)" class="font-weight-bold ml-5" @click="readyUpdateBoardName()" >{{ board.name }}</h1>
      </template>

      <span v-show="isAll" class="is-all">（現在、アーカイブを含んでいます。）</span>
      <v-spacer></v-spacer>

      <!-- board menu -->
      <v-menu v-model="menuDrawer" offset-y>
        <template v-slot:activator="{ on }">
          <v-btn class="mr-5" small fab v-on="on">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>

        <v-card width="300">
          <v-list flat>
            <v-list-item-group>
              <v-list-item v-if="isAll" @click="init()">
                <v-list-item-content>アーカイブを含めない</v-list-item-content>
              </v-list-item>
              <v-list-item v-else @click="retrieveAll()">
                <v-list-item-content>アーカイブを含める</v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-content @click="allAutoSwitch(true)">すべてのリストの自動切換えをON</v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-content @click="allAutoSwitch(false)">すべてのリストの自動切換えをOFF</v-list-item-content>
              </v-list-item>

              <v-list-item>
                <v-list-item-content @click="allCardsNext()">すべてのカードを一つ進める</v-list-item-content>
              </v-list-item>

              <template v-if="homeDefaultBoard">
              <v-divider></v-divider>
              <v-list-item>
                <v-list-item-content @click="$emit('show-not-board')">デフォルトボード設定画面</v-list-item-content>
              </v-list-item>
              </template>

              <v-list-item>
                <v-btn class="red lighten-3" block @click="confirmDialog = true">ボードの削除</v-btn>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card>
      </v-menu>
    </v-row>
    <v-divider></v-divider>

    <!-- board -->
    <div class="board amber lighten-4" :style="{'height': boardHeight}">
      <!-- list -->
      <draggable v-model="board.lists" :options="dragOptions" @update="saveListsOrder(board)">
        <v-card
          v-for="list in board.lists"
          :key="list.id"
          width="270"
          :class="'list grey ' + (list.is_archive ? 'lighten-1' : 'lighten-3')"
        >
          <v-row>
            <v-col cols="10" class="pa-3">
              <v-card-text class="list-title pa-0">{{ list.name }}</v-card-text>
            </v-col>
            <v-col cols="2" class="pl-1">
              <v-icon class="mr-5" @click.stop="copyToListForm(list)">mdi-pencil-outline</v-icon>
            </v-col>
          </v-row>

          <!-- cards -->
          <div class="cards">
            <draggable
              v-model="list.cards"
              :options="dragOptions"
              @start="drag = true"
              @end="drag = false"
              @update="saveCardsOrder(list)"
              @add="saveCardsOrder(list)"
              @remove="saveCardsOrder(list)"
              group="board"
            >
              <v-card
                v-for="card in list.cards"
                :key="card.id"
                :class="'card ' + (card.is_archive ? 'grey lighten-1' : '')"
              >
                <v-row>
                  <v-col cols="10" class="pl-4">
                    <span>{{ card.name }}</span>
                  </v-col>
                  <v-col cols="2" class="pa-0 mt-3">
                    <v-icon @click.stop="copyToCardForm(card, list)">mdi-pencil</v-icon>
                  </v-col>
                </v-row>
              </v-card>
            </draggable>
          </div>

          <!-- add card -->
          <v-card v-if="list.activeList" class="py-2" outlined>
            <input
              v-model="list.newCard.name"
              @blur="addCard(list)"
              @keydown.enter="addCardContinue($event, list)"
              placeholder="カード名"
              ref="addCard"
              class="add-card"
            />
          </v-card>

          <v-btn v-else @click="activateList(list)" color="grey" block>
            <v-icon class="ma-0 pa-0">mdi-plus</v-icon>
          </v-btn>
        </v-card>
      </draggable>
    </div>

    <!-- low button -->
    <v-row class="add-list">
      <v-tooltip top>
        <template v-slot:activator="{ on }">
          <v-btn
            link
            fab
            dark
            @click="addListFormDialog = true; addListForm = {}"
            v-on="on"
            class="blue-grey lighten-2 mr-2"
          >
            <v-icon dark>mdi-plus</v-icon>
          </v-btn>
        </template>
        <span>Add List</span>
      </v-tooltip>
    </v-row>

    <!-- list form dialog -->
    <v-dialog v-model="listFormDialog" width="530">
      <v-card>
        <v-row class="mx-5 pt-2">
          <template v-if="listForm.list['next_list']">
            <v-btn class="grey lighten-2" text @click="cardsNext()">このリストのカードを次に移動</v-btn>
          </template>
          <v-spacer></v-spacer>
          <v-btn fab dark color="grey" @click="listFormDialog = false" x-small>
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-row>
        <v-card-actions>
          <v-text-field label="リスト名" v-model.trim="listForm.copyList.name"></v-text-field>
        </v-card-actions>

        <v-card-actions>
          <v-select
            label="切り替え先リスト"
            v-model="listForm.copyList.next_list"
            :items="switchListItems"
            item-value="id"
            item-text="name"
          ></v-select>
        </v-card-actions>

        <v-card-actions>
          <v-checkbox label="自動切換え" v-model="listForm.copyList.auto_switch"></v-checkbox>
        </v-card-actions>

        <label class="ml-2 grey--text text--darken-1" for="switch-time">切り替え時間</label>
        <v-card-actions>
          <v-time-picker
            id="switch-time"
            :width="switchTimeWidth"
            landscape
            v-model="listForm.copyList.switch_time"
          ></v-time-picker>
        </v-card-actions>
        <v-divider></v-divider>
        <v-card-actions>
          <template>
            <v-btn
              v-if="listForm.list['is_archive']"
              class="grey lighten-2"
              text
              @click="cancelArchiveList()"
            >アーカイブ解除</v-btn>
            <v-btn v-else class="grey lighten-2" text @click="archiveList()">アーカイブ</v-btn>
          </template>
          <v-btn class="red lighten-2" text @click="deleteList()">削除</v-btn>
          <v-spacer></v-spacer>
          <v-btn text @click="updateList()">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- add list form dialog -->
    <v-dialog v-model="addListFormDialog" width="500">
      <v-card>
        <v-row class="px-5 pt-2">
          <v-spacer></v-spacer>
          <v-btn fab dark color="grey" @click="addListFormDialog = false" x-small>
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-row>

        <v-card-actions>
          <v-text-field class="heading" label="リスト名（必須）" v-model.trim="addListForm.name"></v-text-field>
        </v-card-actions>

        <v-card-actions>
          <v-select
            label="切り替え先リスト"
            v-model="addListForm.next_list"
            :items="switchListItems"
            item-value="id"
            item-text="name"
          ></v-select>
        </v-card-actions>

        <v-card-actions>
          <v-checkbox label="自動切換え" v-model="addListForm.auto_switch"></v-checkbox>
        </v-card-actions>

        <label class="ml-2 grey--text text--darken-1" for="switch-time">切り替え時間</label>
        <v-card-actions>
          <v-time-picker
            id="switch-time"
            :width="switchTimeWidth"
            landscape
            v-model="addListForm.switch_time"
          ></v-time-picker>
        </v-card-actions>

        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="addList()">追加</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- card form dialog -->
    <v-dialog v-model="cardFormDialog" width="500">
      <v-card>
        <v-row class="px-5 pt-2">
          <v-spacer></v-spacer>
          <v-btn fab dark color="grey" @click="cardFormDialog = false" x-small>
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-row>

        <v-card-actions>
          <v-text-field label="カード名" v-model.trim="cardForm.copyCard.name"></v-text-field>
        </v-card-actions>

        <v-card-actions>
          <v-textarea label="詳細" auto-grow v-model="cardForm.copyCard.detail"></v-textarea>
        </v-card-actions>

        <v-divider></v-divider>
        <v-card-actions>
          <template>
            <v-btn
              v-if="cardForm.card['is_archive']"
              class="grey lighten-2"
              text
              @click="cancelArchiveCard()"
            >アーカイブ解除</v-btn>
            <v-btn v-else class="grey lighten-2" text @click="archiveCard()">アーカイブ</v-btn>
          </template>
          <v-btn class="red lighten-2" text @click="deleteCard()">削除</v-btn>
          <v-spacer></v-spacer>
          <v-btn text @click="updateCard()">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="confirmDialog" @click="confirmDialog = false" width="400">
      <v-card>
        <v-card-title class="headline">このボードを削除しますか？</v-card-title>
        <v-card-actions>
          <div class="flex-grow-1"></div>
          <v-btn color="grey darken-4" text @click="deleteBoard()">する</v-btn>
          <v-btn color="grey darken-4" text @click="confirmDialog = false">しない</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- please wait -->
    <v-dialog v-model="isLoading" persistent width="300">
      <v-card color="gray" dark>
        <v-card-text>
          Please wait
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import draggable from "vuedraggable";
import { Api } from "@/asynchronous/api";
import { datetimeToJapan } from "@/helper/format";
import { getDevice } from "@/helper/device";

export default {
  props: {
    homeDefaultBoard: Number,
    homeUsername: String
  },
  data() {
    return {
      isLoading: false,
      username: this.$route.params.username,
      boardId: this.$route.params.boardId,
      board: {},
      isInputBoardName: false,
      beforeBoardName: '',
      isAll: false,
      listForm: {
        list: {},
        copyList: {}
      },
      listFormDialog: false,
      addListForm: {},
      addListFormDialog: false,
      cardForm: {
        parentList: {},
        card: {},
        copyCard: {}
      },
      cardFormDialog: false,
      confirmDialog: false,

      dragOptions: {
        animation: 200
      },
      menuDrawer: false,
      boardHeight: "81vh"
    };
  },
  computed: {
    cards() {
      return this.retrieveCard;
    },
    switchListItems() {
      if (this.board.lists === undefined) return;

      let items = [{ id: null, name: "" }];
      for (let list of this.board.lists) {
        if (this.listForm.list.id === list.id) continue;
        items.push({ id: list.id, name: list.name });
      }
      return items;
    },
    switchTimeWidth() {
      if (getDevice() === "other") {
        return 250;
      } else {
        return 150;
      }
    }
  },
  components: {
    draggable
  },
  filters: {
    datetimeToJapan
  },
  methods: {
    retrieveBoard(all = false) {
      this.isLoading = true;
      const self = this;
      const options =
        "include=id,name,lists,auto_switch,switch_time,next_list,is_archive";
      const method = all ? "all_lists" : null;
      return Api.getJson("boards", this.boardId, this.username, options, method)
        .then(response => {
          self.board = response.data;
          self.isLoading = false;
        })
        .catch(error => {
          alert("データが正しく取得できませんでした。");
          self.isLoading = false;
        });
    },
    retrieveAll() {
      const self = this;
      return this.retrieveBoard(true).then(response => {
        for (let list of self.board.lists) {
          self.loadCards(list, true);
        }
        self.isAll = true;
      });
    },
    loadCards(list, all = false) {
      const self = this;
      const options = "include=cards,name,id,moved_at,detail,is_archive";
      const method = all ? "all_cards" : null;
      return Api.getJson("lists", list.id, this.username, options, method)
        .then(response => {
          self.$set(list, "cards", response.data.cards);
        })
        .catch(error => {
          alert("データが正しく取得できませんでした。");
          that.isLoading = false;
        });
    },

    isExistClassName(className, classList) {
      for (let clazz of classList) {
        if (clazz === className) {
          return true;
        }
      }
      return false;
    },

    readyUpdateBoardName() {
      this.beforeBoardName = this.board.name;
      this.isInputBoardName = true;
      this.$nextTick(() => {
        this.$refs.boardName.focus();
      })
    },
    updateBoardName(event) {
      if (event !== undefined && event.keyCode === 229) return
      const name = this.board.name;
      if (name === this.beforeBoardName) {
        this.isInputBoardName = false;
        return
      }
      if (!(name)) {
        this.board.name = this.beforeBoardName
        this.isInputBoardName = false;
        return
      }
      const data = {name: name}
      const self = this;
      Api.patchJson('boards', this.board.id, data, this.username).then(response => {
        self.isInputBoardName = false;
      })
    },

    activateList(list) {
      this.$set(list, "activeList", true);
      this.$set(list, "newCard", {
        list: list.id,
        name: "",
        order: list.cards.length - 1
      });
      this.$nextTick(() => {
        this.$refs.addCard[0].focus();
      });
    },
    addList() {
      if (this.addListForm.name === "") {
        alert("リスト名は必須です。");
        return;
      }
      this.isLoading = true;
      const self = this;
      this.addListForm["board"] = this.boardId;
      Api.postJson("lists", this.addListForm, this.username)
        .then(response => {
          self.board.lists.push(response.data);
          self.addListFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    addCard(list) {
      if (list.newCard.name === "") {
        list.activeList = false;
        return;
      }

      Api.postJson("cards", list.newCard, this.username).then(response => {
        list.cards.push(response.data);
        list.newCard.name = "";
        list.activeList = false;
      });
    },
    addCardContinue(event, list) {
      if (event.keyCode !== 13) return;
      if (list.newCard.name === "") return;

      Api.postJson("cards", list.newCard, this.username).then(response => {
        list.cards.push(response.data);
        list.newCard.name = "";
      });
    },

    saveListsOrder(board) {
      Api.putJson("lists", null, board.lists, this.username, "save_order");
    },
    saveCardsOrder(list) {
      Api.putJson("cards", null, list, this.username, "save_order");
    },

    copyToListForm(list) {
      this.listForm.list = list;
      this.listForm.copyList = Object.assign({}, list);
      delete this.listForm.copyList["cards"];
      this.listFormDialog = true;
    },
    copyToCardForm(card, list) {
      this.cardForm.card = card;
      this.cardForm.copyCard = Object.assign({}, card);
      this.cardForm.parentList = list;
      this.cardFormDialog = true;
    },
    updateList() {
      this.isLoading = true;
      const nextListId = this.listForm.copyList.next_list;
      if (nextListId === null) {
        this.listForm.copyList["next"] = null;
      } else if (typeof nextListId === "number") {
        this.listForm.copyList["next"] = nextListId;
      }
      Api.patchJson(
        "lists",
        this.listForm.copyList.id,
        this.listForm.copyList,
        this.username
      )
        .then(response => {
          Object.assign(this.listForm.list, response.data);
          this.listFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    updateCard() {
      this.isLoading = true;
      Api.patchJson(
        "cards",
        this.cardForm.copyCard.id,
        this.cardForm.copyCard,
        this.username
      )
        .then(response => {
          Object.assign(this.cardForm.card, response.data);
          this.cardFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    eraseList(list) {
      const lists = this.board.lists;
      const listsLen = lists.length;
      for (let i = 0; i < listsLen; i++) {
        if (lists[i].id === list.id) {
          lists.splice(i, 1);
          return;
        }
      }
    },
    eraseCard(card, cards) {
      const cardsLen = cards.length;
      for (let i = 0; i < cardsLen; i++) {
        if (cards[i].id === card.id) {
          cards.splice(i, 1);
          return;
        }
      }
    },

    extractData(data, include = []) {
      let ret = {};
      for (const target of include) {
        for (let key in data) {
          if (target === key) {
            ret[key] = data[key];
          }
        }
      }
      return ret;
    },
    archiveList() {
      this.isLoading = true;
      const self = this;
      const lists = this.board.lists;
      this.listForm.list["is_archive"] = true;
      const data = this.extractData(this.listForm.list, ["is_archive"]);
      Api.patchJson("lists", this.listForm.list.id, data, this.username)
        .then(response => {
          const list = self.listForm.list;
          if (!self.isAll) {
            self.eraseList(list);
          }
          self.listFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    archiveCard() {
      const self = this;
      this.isLoading = true;
      this.cardForm.card["is_archive"] = true;
      const data = this.extractData(this.cardForm.card, ["is_archive"]);
      Api.patchJson("cards", this.cardForm.card.id, data, this.username)
        .then(response => {
          if (!self.isAll) {
            const card = self.cardForm.card;
            const cards = self.cardForm.parentList.cards;
            self.eraseCard(card, cards);
          }
          self.cardFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    cancelArchiveList() {
      this.isLoading = true;
      const lists = this.board.lists;
      this.listForm.list["is_archive"] = false;
      const self = this;
      Api.patchJson(
        "lists",
        this.listForm.list.id,
        this.listForm.list,
        this.username
      )
        .then(response => {
          self.listFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    cancelArchiveCard() {
      this.isLoading = true;
      this.cardForm.card["is_archive"] = false;
      const self = this;
      Api.patchJson(
        "cards",
        this.cardForm.card.id,
        this.cardForm.card,
        this.username
      )
        .then(response => {
          self.cardFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    deleteBoard() {
      this.isLoading = true;
      const self = this;
      Api.delete("boards", this.boardId, this.username)
        .then(response => {
          if (self.homeDefaultBoard) {
            self.$emit('delete-default-board');
            self.confirmDialog = false;
          } else {
            this.$router.push({name: "boardList",params: { username: this.username }});
          }
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    deleteList() {
      this.isLoading = true;
      const listId = this.listForm.list.id;
      const self = this;
      Api.delete("lists", listId, this.username)
        .then(response => {
          const list = self.listForm.list;
          self.eraseList(list);
          self.listFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    deleteCard() {
      this.isLoading = true;
      const self = this;
      Api.delete("cards", this.cardForm.card.id, this.username)
        .then(response => {
          const card = self.cardForm.card;
          const cards = self.cardForm.parentList.cards;
          self.eraseCard(card, cards);
          self.cardFormDialog = false;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    allAutoSwitch(autoSwitch = true) {
      this.isLoading = true;
      let method = "auto_switch/";
      if (autoSwitch) {
        method += "true";
      } else {
        method += "false";
      }
      const self = this;
      Api.putJson("boards", this.boardId, null, this.username, method)
        .then(response => {
          for (let list of self.board.lists) {
            list["auto_switch"] = autoSwitch;
          }
        })
        .finally(() => {
          self.isLoading = false;
        });
    },

    moveCards(previousList) {
      const nextList = previousList["next_list"];
      if (!nextList) return;
      const nextId = nextList.id;
      for (let list of this.board.lists) {
        if (nextId === list.id) {
          const cardsLen = previousList.cards.length;
          const nextCards = previousList.cards.splice(0, cardsLen);
          list.cards.push(...nextCards);
          return;
        }
      }
    },

    cardsNext() {
      this.isLoading = true;
      const listId = this.listForm.list.id;
      const self = this;
      Api.putJson("lists", listId, null, this.username, "next")
        .then(response => {
          self.moveCards(this.listForm.list);
        })
        .finally(() => {
          self.isLoading = false;
        });
    },

    allCardsNext() {
      this.isLoading = true;
      const self = this;
      Api.putJson("boards", this.boardId, null, this.username, "all_cards_next")
        .then(response => {
          let intendNextList = [];
          for (const list of self.board.lists) {
            if (!list["next_list"]) continue;
            if (!list["auto_switch"]) continue;

            const nextId = list["next_list"].id;
            for (const nextList of self.board.lists) {
              if (nextList.id === nextId) {
                const cardsLen = list.cards.length;
                nextList.tempCards = list.cards.splice(0, cardsLen);
                intendNextList.push(nextList);
              }
            }
          }
          for (const list of intendNextList) {
            list.cards.push(...list.tempCards);
            delete list.tempCards;
          }
        })
        .finally(() => {
          self.isLoading = false;
        });
    },

    init() {
      if (this.homeDefaultBoard) {
        this.boardId = this.homeDefaultBoard;
        this.username = this.homeUsername;
        this.boardHeight = "75vh";
      }
      this.isAll = false;
      const self = this;
      this.retrieveBoard().then(response => {
        for (let list of self.board.lists) {
          self.loadCards(list);
        }
      });
    }
  },
  created() {
    this.init();
  }
};
</script>

<style scoped lang="sass">
.is-all
  line-height: 3
.board
  padding-top: 20px
  overflow-y: hidden
  overflow-x: scroll
  white-space: nowrap
.list
  display: inline-block
  vertical-align: top
  margin: 0px 5px
  padding: 5px
.list:hover
  cursor: grab
.cards
  max-height: 420px
  overflow-y: scroll
  overflow-x: hidden
.card
  margin: 5px 0px
  white-space: normal
.list-title
  text-overflow: ellipsis
  overflow: hidden
  border-bottom: solid 2px grey
.wrapper
  position: relative
.add-list
  position: absolute
  right: 20px
  bottom: 20px
.add-card
  width: 95%
  margin-left: 5px
</style>
