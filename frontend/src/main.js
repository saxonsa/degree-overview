import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import Router from 'vue-router'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@fortawesome/fontawesome-free/css/all.css'
import '../src/assets/icon/iconfont.css'
import '../src/css/bootstrap.css'
// import { Spin } from 'iview'
import Loading from 'vue-loading-spin'
import 'vue-loading-spin/dist/loading.css'
// import 'ant-design-vue/dist/antd.css'
import { Spin, Upload, Icon, message, notification, Timeline, Card, Descriptions, Badge, Table, Tag } from 'ant-design-vue'
import { DatePicker, Input, Form, FormItem, Col, InputNumber, Select, Option } from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
import * as echarts from 'echarts' // 奇奇怪怪的Echarts引入, 不知道能不能用

const routerPush = Router.prototype.push
Router.prototype.push = function push (location) {
  return routerPush.call(this, location).catch(error => error)
}

// 按需调取antd的组件
Vue.use(Spin)
Vue.use(Upload)
Vue.use(Icon)
Vue.use(Timeline)
Vue.use(Card)
Vue.use(Descriptions)
Vue.use(Badge)
Vue.use(Table)
Vue.use(Tag)
Vue.prototype.$Message = message
Vue.prototype.$Notification = notification

// 调取element ui组件
locale.use(lang) // use english version for element ui
Vue.use(DatePicker)
Vue.use(Input)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Col)
Vue.use(InputNumber)
Vue.use(Select)
Vue.use(Option)

// 全局使用Echarts
Vue.prototype.$Echarts = echarts

// 全局引用 spin 组件
// 调用方法: this.$Spin.show()
// Vue.prototype.$Spin = Spin

Vue.use(Loading, {
  isFixed: true,
  isComponent: true,
  isShowAnimation: true,
  indicatorText: 'Loading...'
})

Vue.config.productionTip = false

axios.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded'

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
