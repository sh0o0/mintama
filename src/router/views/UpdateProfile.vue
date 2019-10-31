<template>
  <v-app>
    <h2 class="heading">プロフィール編集</h2>
      <v-row class="mb-10">
        <v-col align-self="start" class="p-2" cols="12" md="3">
          <v-card class="pa-2">
            <v-row>
              <v-col cols="6" md="12">
                <v-avatar color="grey" size="170" tile>
                  <v-img v-if="formObj.icon.value" :src="formObj.icon.value" alt="USER ICON"></v-img>
                </v-avatar>
              </v-col>
              <v-col cols="6" md="12">
                <v-file-input show-size :label="formObj.icon.label" @change="inputFile"></v-file-input>
                <v-checkbox v-model="formObj.icon.clear" label="アイコンを消す"></v-checkbox>
                <FormError :formName="formObj.icon.name" :errors="formObj.icon.errors"></FormError>
              </v-col>
            </v-row>
          </v-card>
        </v-col>
        <v-col cols="12" md="9">
          <v-form v-model="valid">

          <FormError :formName="formObj.username.name" :errors="formObj.username.errors"></FormError>
          <v-text-field
            :label="formObj.username.label"
            v-model.trim="formObj.username.value"
            :type="formObj.username.type"
            :prepend-icon="formObj.username.prependIcon"
          />

          <FormError :formName="formObj.email.name" :errors="formObj.email.errors"></FormError>
          <v-text-field
            :label="formObj.email.label"
            v-model.trim="formObj.email.value"
            :type="formObj.email.type"
            :prepend-icon="formObj.email.prependIcon"
          />

          <FormError :formName="formObj.gender.name" :errors="formObj.gender.errors"></FormError>
          <v-select
            :items="GENDER_CHOICIES"
            item-value="value"
            item-text="text"
            :label="formObj.gender.label"
            :prepend-icon="formObj.gender.prependIcon"
            v-model="formObj.gender.value"
          ></v-select>

          <FormError :formName="formObj.residence.name" :errors="formObj.residence.errors"></FormError>
          <v-select
            :items="RESIDENCE_CHOICIES"
            :label="formObj.residence.label"
            :prepend-icon="formObj.residence.prependIcon"
            v-model="formObj.residence.value"
          ></v-select>

          <FormError :formName="formObj.learning_started_date.name" :errors="formObj.learning_started_date.errors"></FormError>
          <learning-started-date-form 
          :form="formObj.learning_started_date"
          ></learning-started-date-form>
          
          <FormError :formName="formObj.crack_level.name" :errors="formObj.crack_level.errors"></FormError>
          <crack-level-form
          :form="formObj.crack_level"
          ></crack-level-form>

          <FormError :formName="formObj.introduction.name" :errors="formObj.introduction.errors"></FormError>
          <v-textarea
          :label="formObj.introduction.label"
          v-model="formObj.introduction.value"
          :rules="introductionRules"
          counter
          outlined
          clearable
          clear-icon="cancel"
          auto-grow
          />
          </v-form>
          <v-btn  v-show="valid" link @click="update" color="orange" absolute bottom right>変更</v-btn>
          <v-btn  v-show="!(valid)" link color="grey lighten-4" absolute bottom right>変更</v-btn>
          <Dialog 
          heading="変更が完了しました。"
          :dialog="dialog"
          @dialog-to-false="dialog = false"
          ></Dialog>

        </v-col>
      </v-row>
  </v-app>
</template>
<script>
import { mapActions, mapGetters, mapMutations } from "vuex";

import CrackLevelForm from "@/components/CrackLevelForm";
import LearningStartedDateForm from "@/components/LearningStartedDateForm";
import FormError  from '@/components/FormError'
import Dialog from '@/components/Dialog'

import FormHelper from '@/helper/form'
import FormOptions from '@/helper/form_options'
import { GENDER_CHOICIES, RESIDENCE_CHOICIES } from '@/helper/constant'

export default {
  data() {
    return {
      introductionRules: [v => !v || v.length <= 500 || "Max 500 characters"],
      formObj: {},
      dialog: false,
      valid: true,
    };
  },
  components: {
    CrackLevelForm,
    LearningStartedDateForm,
    FormError,
    Dialog,
  },
  computed: {
    ...mapGetters("accounts", ["getMyself"]),
    GENDER_CHOICIES() {
      return　GENDER_CHOICIES;
    },
    RESIDENCE_CHOICIES() {
      return RESIDENCE_CHOICIES;
    }
  },
  methods: {
    ...mapActions("accounts", ["apiGetMyself", "apiPatchMyself"]),
    ...mapMutations('accounts', ['setBaselineMyself']),
    update() {
      const that = this;
      FormHelper.clearErrors(this.formObj)
      this.apiPatchMyself({username: this.getMyself.username, formObj: this.formObj}).then(response => {
        that.dialog = true;
        that.apiGetMyself().then(response => {
          that.setBaselineMyself();
        })
      })
    },
    inputFile(file) {
      FormHelper.setFileToThatFormObj(this.formObj['icon'], file)
    },
  },
  created() {
    const that = this;
    FormHelper.createThatFormObjs(that, ...FormOptions.user)
    this.apiGetMyself().then(response => {
      FormHelper.assignDataToThatObj(that, that.getMyself)
    })
  }
};
</script>