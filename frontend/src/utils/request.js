import { notification } from 'ant-design-vue'
import axios from 'axios'
import qs from 'qs'
import router from '../router'
import store from '../store'
import storage from '@/utils/storage.js'
const service = axios.create({
  // baseURL: 'http://localhost:5000/', // api 的 baseUrl 就是每个请求前面相同的地址
  baseURL: '/api',
  timeout: 5000 // 请求超时时间
})
// request 拦截器
service.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
service.interceptors.request.use(
  config => {
    // 这里是每个请求的设置, 比如每个请求都携带一个token, 或者当为post请求时, 引入qs格式化参数
    if (storage.get('JWT_TOKEN')) {
      config.headers.common.Authorization = `Bearer ${storage.get('JWT_TOKEN')}`
    }

    let request = {}
    request.jsondata = JSON.stringify(config.data)
    request = qs.stringify(request)
    config.data = request

    return config
  },
  error => {
    console.log('request error: ' + error)
    Promise.reject(error)
  }
)

// response 拦截器
service.interceptors.response.use(
  response => {
    // 这个地方的status自己与后台约定(可以根据状态码, 设置自己要提示的信息)
    switch (response.status) {
      case 200: {
        store.commit('set_token', storage.get('JWT_TOKEN'))
        return Promise.resolve(response.data)
      }
      case 401: {
        store.commit('del_token')
        router.push({ name: 'Login' })
        break
      }
      case 500: {
        router.push({ name: 'Error500' })
        break
      }
    }
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          notification.error({
            message: 'Authorization fail',
            description: 'User certification fail, please login again!'
          })
          store.commit('del_token')
          router.replace({
            path: '/login',
            query: { redirect: router.currentRoute.fullPath }
          })
      }
    }
    return Promise.reject(error.response.data)
  }
)

export { service as axios }
