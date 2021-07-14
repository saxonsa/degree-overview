import { axios } from '@/utils/request'

export function uploadCILO (params) {
  return axios({
    url: '/cilo/upload_cilo',
    method: 'post',
    params: params
  })
}

export function getCILOTemplate (params) {
  return axios({
    url: '/cilo/get_cilo_template',
    method: 'get',
    params: params,
    responseType: 'blob'
  })
}

export function getCourseCILO (params) {
  return axios({
    url: '/cilo/get_course_cilo',
    method: 'get',
    params: params
  })
}

export function getCILOContentByIndex (params) {
  return axios({
    url: '/cilo/get_specific_cilo_content_by_index',
    method: 'get',
    params: params
  })
}
