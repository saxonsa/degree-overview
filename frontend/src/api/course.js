import { axios } from '@/utils/request'

export function createCourse (params) {
  return axios({
    url: '/course/create_course',
    method: 'post',
    params: params
  })
}

export function modifyCourse (params) {
  return axios({
    url: '/course/modify_course',
    method: 'put',
    params: params
  })
}

export function getCourseDetailByCourseCode (params) {
  return axios({
    url: '/course/get_course_detail_by_course_code',
    method: 'get',
    params: params
  })
}

export function getCourseDependencyAll (params) {
  return axios({
    url: '/course/get_course_dependency_all',
    method: 'get',
    params: params
  })
}

export function getAllProgram (params) {
  return axios({
    url: '/course/get_all_program',
    method: 'get',
    params: params
  })
}
