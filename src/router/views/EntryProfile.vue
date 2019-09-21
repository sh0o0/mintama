<template>
  <v-app>
    <v-card class="pa-2 pb-8">
      <v-card-title>プロフィール編集</v-card-title>
      <v-row>
        <v-col align-self="start" class="p-2" cols="12" md="3">
          <v-card class="pa-2">
            <v-row>
              <v-col cols="4" md="12">
                <v-avatar color="grey" size="170" tile>
                  <v-img v-if="getIconSrc" :src="getIconSrc" alt="USER ICON"></v-img>
                </v-avatar>
              </v-col>
              <v-col cols="8" md="12">
                <v-file-input show-size label="アイコン" @change="setInputImageData"></v-file-input>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
        <v-col cols="12" md="9">
          <v-text-field
            label="ユーザー名"
            v-model.trim="myself.username"
            type="text"
            prepend-icon="mdi-rename-box"
          />
          <v-text-field
            label="メールアドレス"
            v-model.trim="myself.email"
            type="email"
            prepend-icon="mdi-email-edit"
          />
          <v-select
            :items="GENDER_CHOICIES"
            label="性別"
            item-value="value"
            item-text="text"
            prepend-icon="mdi-gender-male-female"
            v-model="myself.gender"
          ></v-select>

          <v-select
            :items="RESIDENCE_CHOICIES"
            label="居住地"
            prepend-icon="mdi-home-account"
            v-model="myself.residence"
          ></v-select>

          <learning-started-date-form></learning-started-date-form>

          <crack-level-form></crack-level-form>

          <v-textarea
            label="自己紹介"
            v-model="getMyself.introduction"
            outlined
            clearable
            clear-icon="cancel"
            :rules="introductionRules"
            counter
            auto-grow
          />
          <v-btn link @click="update" color="orange" absolute bottom right>変更</v-btn>
        </v-col>
      </v-row>
    </v-card>
  </v-app>
</template>
<script>
import { mapActions, mapGetters, mapState, mapMutations } from "vuex";
import CrackLevelForm from "@/components/CrackLevelForm";
import LearningStartedDateForm from "@/components/LearningStartedDateForm";
import FormHelper from '@/helper/form'
import { GENDER_CHOICIES, RESIDENCE_CHOICIES } from '@/helper/constant'

export default {
  data() {
    return {
      introductionRules: [v => !v || v.length <= 300 || "Max 300 characters"],
      formObj: {
      },
    };
  },
  components: {
    CrackLevelForm,
    LearningStartedDateForm
  },
  computed: {
    ...mapGetters("user", [
      "getMyself",
      "getIconSrc"
    ]),
    ...mapState("user", ["myself"]),
    GENDER_CHOICIES() {
      return　GENDER_CHOICIES;
    },
    RESIDENCE_CHOICIES() {
      return RESIDENCE_CHOICIES;
    }
  },
  methods: {
    ...mapActions("user", ["apiGetMyself", "apiPutMyself"]),
    ...mapMutations("user", ["setInputImageData", 'setMyselfOptionsAdded']),
    update() {
      this.apiPutMyself().then(response => {
      })
    }
  },
  created() {
    const that = this;
    this.apiGetMyself().then(response => {
      FormHelper.createThatFormObj(that, {name: 'section', label: 'first', type: 'text'})
      FormHelper.assignDataToThatObj(that, that.getMyself)
    }).catch(error => {
      console.log(error)
    })
  }
};
</script>