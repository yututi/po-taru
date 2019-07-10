import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'
import 'vuetify/src/stylus/components/_buttons.styl'
import ja from 'vuetify/src/locale/ja'

Vue.use(Vuetify, {
  iconfont: 'fa',
  lang: {
    locales: { ja },
    current: 'ja'
  },
})
