import { axios } from '@/utils/request'

export function userLogin (params) {
  return axios({
    url: '/user/login',
    method: 'post',
    params: params
  })
}

export function userRegister (params) {
  return axios({
    url: '/user/register',
    method: 'post',
    params: params
  })
}

export function userResetPassword (params) {
  return axios({
    url: '/user/reset_password',
    method: 'get',
    params: params
  })
}
