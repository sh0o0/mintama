
const user = [
  {name: 'icon', type: 'file', label: 'アイコン', clear: false},
  {name: 'username', label: 'ユーザー名', prepenIcon: 'mdi-rename-box'},
  {name: 'email', label: 'メールアドレス', type: 'email', prepenIcon: 'mdi-email-edit', type: 'email'},
  {name: 'gender', label: '性別', prepenIcon: 'mdi-gender-male-female'},
  {name: 'residence', prepenIcon: 'mdi-home-account', label: '居住地'},
  {name: 'crack_level', prepenIcon: 'alert-decagram', label: 'ひび割れ度'},
  {name: 'learning_started_date', prepenIcon: 'event', label: '学習開始時期'},
  {name: 'introduction', label: '自己紹介'}
]

export default {
  user,
}