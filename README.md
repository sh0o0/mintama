# みんたま
> URL : [mintama.work](http://mintama.work)

## 誰のためのものか
プログラミング独学初学者が、効率的に勉強を進められるようにとの思いで作成しました。
私が独学でこれまで勉強をしてきたたため、一緒に独学で学んでいる方の助力になればという思いで当サービスを作成しました。
***
## 経緯
2019年4月からプログラミングの学習を始めました。

***
## 開発環境
- PC
    - Windows10
- 言語
    - Python
    - JavaScript ( node.js )
- フレームワーク
    - Django
    - Rest framework
    - Vue.js
- デプロイ
    - AWS
***
## 開発について
### ■　アーキテクチャ
- M : Django.models
- V : Vue.js
- C : Rest framework , Django.Views

### ■　API
データのやり取りはDjango Rest frameworkを使用したAPIを作成し、Vue.js × axiosを使用して表示させています。<br>
主にSerializersで躓きましたが、技術ブログやリファレンス、Rest frameworkの生のコードを読みなどして何とか実装出来ました。

### ■　Django
Django本来の機能を使用した箇所は、Model、Form、サインアップ、ログインなどです。Djangoで簡略化されている機能については、甘えさせてもらい使わせてもらっています。

### ■　Vue.js
View側はVue.js, vuetifyを使用しました。webpack導入段階でエラーが出まくり2週間ほど苦戦していました。このときは本当につらかったです（泣）<br>
結局、webpackの基礎をudemyで勉強しなおし、一から実装することによって乗り越えました。やっぱり基礎は大事！
Vuexについては、vuetifyを使ったことにより、componentのネストがほぼほぼなくなり、あまり使わなかったです。<br>
Vue.jsを使用した感想は、おもしろい！です。難しくなく、直観的に動作してくれるのでそう感じました。

### ■　AWS
WEBサーバーは、EC2内でDjango、nginx、uwsgiで動かしています。データベースはMariaDBです。画像やCSSなどはS3にアップロードをする仕様にし、CloudFrontを介して取得をします。

***
## 各機能について
各機能について目的、工夫したところなどを紹介します。

### ■　TODO 

### ■　ノート

### ■　リファレンス

***

## 参考資料（開発）

## 参考資料（勉強）