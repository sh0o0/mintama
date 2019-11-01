<template>
  <v-app>
    <!-- sideDrawer -->
    <v-navigation-drawer v-model="sideDrawer" app>
      <v-list dense>
        <router-link :to="{name: 'home'}" class="deco-none">
          <v-list-item link class="pl-5">
            <v-list-item-action>
              <v-icon>mdi-home</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>ホーム</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </router-link>

        <v-list-group
          v-for="item in sideDrawerItems"
          :key="item.title"
          :value="false"
          class="pl-1 ma-0"
        >
          <template v-slot:activator>
            <v-list-item link class="pl-0">
              <v-list-item-action>
                <v-icon>{{item.icon}}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>{{item.title}}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>

          <router-link
            v-for="router in item.routers"
            :key="router.title"
            :to="router.router"
            class="deco-none"
          >
            <v-list-item class="pl-8" link>
              <v-list-item-action>
                <v-list-item-title>{{ router.title }}</v-list-item-title>
              </v-list-item-action>
            </v-list-item>
          </router-link>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="blue" dark>
      <v-app-bar-nav-icon @click.stop="sideDrawer = !sideDrawer" id="side-drawer-btn"></v-app-bar-nav-icon>
      <v-toolbar-title class="px-3">
        <a href="/" class="deco-none font-italic font-weight-bold"><img class="mintama-img" src="https://static.mintama.work/static/mintama/img/white-egg-level-5.png"></a>
      </v-toolbar-title>
      
      <!-- crack levelが実装できていないため保留
      <v-avatar size="80" width="150">
        <img
          v-if="getBaselineMyself"
          :src="`/static/mintama/img/white-egg-level-${getBaselineMyself.crack_level}.png`"
        />
      </v-avatar> -->
      <v-spacer></v-spacer>

      <!-- menuDrawer -->
      <div class="text-center mx-2">
        <v-menu v-model="menuDrawer" offset-y nudge-width="250">
          <template v-slot:activator="{ on }">
            <v-avatar color="orange" v-on="on" class="add-pointer" id="menu-btn">
              <v-img v-if="getBaselineMyself.icon" :src="getBaselineMyself.icon" alt="icon" />
              <v-icon v-else x-large>mdi-egg</v-icon>
            </v-avatar>
          </template>

          <v-card>
            <v-list>
              <v-list-item>
                <v-list-item-avatar>
                  <img v-if="getBaselineMyself.icon" :src="getBaselineMyself.icon" alt="icon" />
                  <v-icon v-else x-large>mdi-egg</v-icon>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title>{{ getBaselineMyself.username }}</v-list-item-title>
                  <v-list-item-subtitle>ひび割れ度：{{ getBaselineMyself.crack_level }}.LV</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>

            <v-divider></v-divider>

            <v-list>
              <router-link
                v-for="item in menuDrawerItems"
                :key="item.title"
                :to="item.router"
                class="deco-none"
              >
                <v-list-item link>
                  <v-list-item-action>
                    <v-icon>{{item.icon}}</v-icon>
                  </v-list-item-action>
                  <v-list-item-content>
                    <v-list-item-title>{{item.title}}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </router-link>
            </v-list>

            <v-card-actions>
              <div class="flex-grow"></div>
              <v-btn text href="/logout/" class="blue darken-4" dark block>Logout</v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </div>
    </v-app-bar>

    <!-- content -->
    <v-content>
      <div class="pa-2">
        <slot name="content"></slot>
      </div>
    </v-content>
  </v-app>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from "vuex";
import { getDevice } from '@/helper/device.js'
export default {
  props: ["username"],
  data() {
    return {
      sideDrawer: false,
      menuDrawer: false,
      sideDrawerItems: [
        {
          title: "TODO",
          icon: "mdi-calendar-range",
          routers: [
            {
              title: "ボードリスト",
              router: { name: "boardList", params: { username: this.username } }
            }
          ]
        },
        {
          title: "ノート",
          icon: "mdi-border-color",
          routers: [
            {
              title: "新規ノートの作成",
              router: {
                name: "createNote",
                params: { username: this.username }
              }
            },
            {
              title: "自分のノート",
              router: {
                name: "personalNoteList",
                params: { username: this.username }
              }
            },
            { title: "みんなのノート", router: { name: "noteList" } }
          ]
        },
        {
          title: "リファレンス",
          icon: "mdi-file",
          routers: [
            {
              title: "自分のリファレンス",
              router: {
                name: "personalReferenceList",
                params: { username: this.username }
              }
            },
            {
              title: "みんなのリファレンス",
              router: { name: "referenceList" }
            }
          ]
        }
      ],
      // { title: "チャット", icon: "mdi-chat", routerName: "" },
      // { title: "計画", icon: "mdi-floor-plan", routerName: "" },
      // { title: "コミュニティ", icon: "mdi-forum", routerName: "" },
      // { title: "チーム開発", icon: "mdi-account-group", routerName: "" }
      menuDrawerItems: [
        {
          title: "アカウント",
          icon: "mdi-account-circle",
          router: { name: "profile", params: { username: this.username } }
        },
        {
          title: "過去の参考資料",
          icon: "mdi-file",
          router: {
            name: "personalReferenceList",
            params: { username: this.username }
          }
        }
        // {
        //   title: "ポートフォリオ",
        //   icon: "mdi-arm-flex",
        //   router: { name: "portfolio" }
        // }
        // { title: "お気に入り", icon: "mdi-heart", router: "" },
        // { title: "設定", icon: "mdi-settings-box", router: "" }
      ]
    };
  },
  methods: {
    ...mapActions("accounts", ["apiGetMyself"]),
    ...mapMutations("accounts", ["setBaselineMyself", 'setUsername']),
  },
  computed: {
    ...mapGetters("accounts", ["getBaselineMyself"])
  },
  created() {
    this.setUsername(this.username);
    this.apiGetMyself().then(response => {
      this.setBaselineMyself();
    });
    if (getDevice() === 'other') {
      this.sideDrawer = true;
    } else {
      this.sideDrawer = false;
    }
  }
};
</script>
<style lang="sass">
.mintama-img
  height: 80px
  width: 80px
  margin-bottom: 10px
  object-fit: cover
  opacity: 0.9
</style>