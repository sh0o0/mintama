<template>
  <div>
    <h2 class="review-title">今日の復習</h2>
    <div class="wrapper">
      <section v-for="(notes, daysKey) in noteList" :key="daysKey" class="notes">
        <h3 class="days-title">{{ daysKey | daysKeyFilter }}</h3>
        <div v-for="note in notes" :key="note.id" class="note">
          <div class="note-title-bar clearfix">
          <h4 class="note-title">{{ note.title }}</h4>
          <router-link class="note-btn deco-none" :to="{name: 'note', params: {noteId: note.id, username: getUsername}}">ノートを見に行く</router-link>
          </div>
          <ul class="section-group">
          <li v-for="section in note.sections" :key="section.id" class="section">
            {{ section.heading }}
          </li>

          </ul>
        </div>
      </section>
      <a class="link" href="http://www.singakukai.com/column/8610.html" target="_blank">復習期間について（ウォズニアック式）</a>
    </div>
  </div>
</template>
<script>
import { mapGetters } from 'vuex'
import { Api } from '@/asynchronous/api'

export default {
  data() {
    return {
      noteList: []
    }
  },
  computed: {
    ...mapGetters('accounts', ['getUsername']),
  },
  filters: {
    daysKeyFilter(daysKey) {
      const days =  daysKey.trim().split('_')[1]
      return `${days} days ago`
    },
  },
  methods: {
    retrieveNoteList() {
      const self = this;
      Api.getJson('reviews', this.getUsername).then(response => {
        self.noteList = response.data;
      })
    }
  },
  created() {
    this.retrieveNoteList()
  },
}
</script>
<style scoped lang="sass">
.review-title
  padding: 12px
  text-align: center
  border-bottom: solid 1px #EEEEEE
  font-size: 1.5rem
  font-weight: bold
.wrapper
  padding: 8px
.days-title
  font-weight: bold
  border-bottom: 1px #555555 double
.note-title-bar
  background-color: #FFECB3
  padding: 6px 0px
.note-title
  display: inline-block
  float: left
  margin: 5px 0px 0px 10px
  text-align: left
.note-btn
  display: inline-block
  text-align: right
  float: right
  background-color: #D7CCC8
  margin-right: 10px
  padding: 3px
  border-radius: 5px
  box-shadow: 1px 1px 3px 3px rgba(192, 192, 192, 0.5)
.notes
  margin-bottom: 30px
.note
 margin-bottom: 10px 
.section-group
  padding: 0px
.section
  padding-left: 40px
  list-style: none
  transition: 0.3s
.section:hover
  background-color: #EEEEEE
  opacity: 0.8
.link
  font-size: 0.8rem
  color: #666666
  text-decoration-color: #666666
</style>