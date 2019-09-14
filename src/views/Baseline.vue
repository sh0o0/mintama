<template>
  <v-app>
    <!-- sideDrawer -->
    <v-navigation-drawer v-model="sideDrawer" app>
      <v-list dense>
        <router-link
          v-for="item in sideDrawerItems"
          :key="item.title"
          :to="{name: item.routerName}"
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
      <template v-slot:append>
        <div class="pa-2">
          <v-btn block href="/logout/" class="blue darken-4" dark>Logout</v-btn>
        </div>
      </template>
    </v-navigation-drawer>

    <v-app-bar app color="blue" dark>
      <v-app-bar-nav-icon @click.stop="sideDrawer = !sideDrawer"></v-app-bar-nav-icon>
      <v-toolbar-title>
        <a class="deco-none" href="/">Mintama</a>
      </v-toolbar-title>
      <v-avatar size="80" width="150">
        <img v-if="getMyself" :src="`/static/mintama/img/white-egg-level-${getMyself.crack_level}.png`" />
      </v-avatar>
      <v-spacer></v-spacer>

      <!-- menuDrawer -->
      <div class="text-center mx-2">
        <v-menu v-model="menuDrawer" offset-y>
          <template v-slot:activator="{ on }">
            <v-avatar color="orange" v-on="on" class="add-pointer">
              <img v-if="getMyself" :src="getMyself.icon" alt="icon"/>
              <v-icon v-else x-large>mdi-egg</v-icon>
            </v-avatar>
          </template>

          <v-card>
            <v-list>
              <v-list-item>
                <v-list-item-avatar>
                  <img v-if="getMyself" :src="getMyself.icon" alt="icon" />
                  <v-icon v-else x-large>mdi-egg</v-icon>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title>{{ getMyself.username }}</v-list-item-title>
                  <v-list-item-subtitle>ひび割れ度：{{ getMyself.crack_level }}.LV</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>

            <v-divider></v-divider>

            <v-list>
              <router-link
                v-for="item in menuDrawerItems"
                :key="item.title"
                :to="{name: item.routerName}"
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
              <v-btn text href="/logout/" class="blue darken-4" dark>Logout</v-btn>
              <v-btn outlined text @click="menuDrawer = false">Cancel</v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </div>
    </v-app-bar>

    <!-- content -->
    <v-content>
      <v-container class="fill-height" fluid>
        <v-row align="center" justify="center">
          <v-col class="text-center">
            <router-view></router-view>
            <slot name="content"></slot>
          </v-col>
        </v-row>
      </v-container>
    </v-content>
    <v-footer color="blue" app>
      <span class="white--text">&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
import { mapActions, mapGetters, mapMutations } from 'vuex'
export default {
  props: {},
  data: () => ({
    sideDrawer: true,
    menuDrawer: false,
    sideDrawerItems: [
      { title: "ホーム", icon: "mdi-home", routerName: "home" },
      { title: "日記", icon: "mdi-border-color", routerName: "" },
      { title: "チャット", icon: "mdi-chat", routerName: "" },
      { title: "計画", icon: "mdi-floor-plan", routerName: "" },
      { title: "コミュニティ", icon: "mdi-forum", routerName: "" },
      { title: "チーム開発", icon: "mdi-account-group", routerName: "" }
    ],
    menuDrawerItems: [
      { title: "アカウント", icon: "mdi-account-circle", routerName: "profile"},
      { title: "過去の参考資料", icon: "mdi-file", routerName: "myReferences" },
      { title: "ポートフォリオ", icon: "mdi-arm-flex", routerName: "myPortfolios" },
      { title: "お気に入り", icon: "mdi-heart", routerName: "" },
      { title: "設定", icon: "mdi-settings-box", routerName: "" }
    ],
  }),
  methods: {
    ...mapActions('user', ['apiGetMyself']),
    ...mapMutations('user', ['setMyselfOptionsAdded']),
  },
  computed: {
    ...mapGetters('user', ['getMyself', 'getMyselfOptionsAdded'])
  },
  created() {
    if (!this.getMyself){
      const that = this;
      (async function() {
        await that.apiGetMyself();
      }())
    }
  }
};
</script>