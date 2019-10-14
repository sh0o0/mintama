<template>
  <v-app>
    <v-card class="pa-2 pb-8">
      <v-card-title>プロフィール</v-card-title>
      <v-row>
        <v-col align-self="start" class="p-2" cols="12" md="3">
          <v-card class="pa-2">
            <v-row>
              <v-col cols="4" md="12">
                <v-avatar color="grey" size="170" tile>
                  <v-img v-if="getMyself.icon" :src="getMyself.icon" alt="USER ICON"></v-img>
                </v-avatar>
              </v-col>
              <v-col cols="8" md="12">
                <v-card-text>{{ getMyself.introduction }}</v-card-text>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
        <v-col cols="12" md="9">
          <v-simple-table>
            <tbody>
              <template v-for="info in formObj">
                <tr v-if="!(exclude.includes(info.name))" :key="info.name">
                  <td>{{ info.label }}</td>
                  <td>{{ info.value ? info.value : '未設定' }}</td>
                </tr>
              </template>
            </tbody>
          </v-simple-table>
          <template v-if="getMyself.username === username">
            <router-link :to="{name: 'settingsProfile'}" class="deco-none">
              <v-btn link color="orange" absolute bottom right>編集</v-btn>
            </router-link>
          </template>
        </v-col>
      </v-row>
    </v-card>
  </v-app>
</template>
<script>
import { mapGetters } from "vuex";
import { Api } from "@/asynchronous/api";
import FormHelper from "@/helper/form";
import FormOptions from "@/helper/form_options";

export default {
  data() {
    return {
      formObj: {},
      exclude: ["icon", "introduction"],
      username: this.$route.params.username
    };
  },
  computed: {
    ...mapGetters("accounts", ["getMyself"])
  },
  created() {
    const that = this;
    FormHelper.createThatFormObjs(that, ...FormOptions.user);

    Api.getJson("users", this.username)
      .then(response => {
        FormHelper.assignDataToThatObj(that, response.data);
      })
      .catch(error => {
        console.log(error.response.data);
      });
  }
};
</script>