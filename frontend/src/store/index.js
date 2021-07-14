import Vue from 'vue'
import Vuex from 'vuex'
import snackbar from '@/store/modules/snackbar.js'
import storage from '@/utils/storage.js'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    snackbar
  },
  state: {
    Authorization: storage.get('JWT_TOKEN') ? storage.get('JWT_TOKEN') : '',
    // token: localStorage.getExpired('token'),
    me: {
      id: storage.get('id'),
      engname: storage.get('engname'),
      nickname: storage.get('nickname'),
      phone: storage.get('phone'),
      email: storage.get('email'),
      role: storage.get('role'),
      designAuth: storage.get('designAuth'),
      program: storage.get('program'),
      gender: storage.get('gender')
    }
  },
  getters: {
    me: state => state.me
  },
  mutations: {
    set_token (state, token) {
      state.Authorization = token
      // 设置token过期时间为一个小时
      storage.set('JWT_TOKEN', token, 1400)
    },
    del_token (state) {
      state.Authorization = ''
      storage.remove('JWT_TOKEN')
    },
    set_personal_info (state, me) {
      state.me.id = me.id
      state.me.engname = me.engname
      state.me.nickname = me.nickname
      state.me.phone = me.phone
      state.me.email = me.email
      state.me.role = me.role
      state.me.designAuth = me.designAuth
      state.me.gender = me.gender
      state.me.program = me.program

      storage.set('id', me.id, 1400)
      storage.set('username', me.username, 1400)
      storage.set('engname', me.engname, 1400)
      storage.set('nickname', me.nickname, 1400)
      storage.set('phone', me.phone, 1400)
      storage.set('email', me.email, 1400)
      storage.set('role', me.role, 1400)
      storage.set('program', me.program, 1400)
      storage.set('gender', me.gender, 1400)
      storage.set('designAuth', me.designAuth, 1400)
    }
  },
  actions: {
  }
})
