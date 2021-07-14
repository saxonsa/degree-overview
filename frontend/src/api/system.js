import { axios } from '@/utils/request'

export function searchCourseByTypeAndKeyword (params) {
  return axios({
    url: '/system/search_course',
    method: 'get',
    params: params
  })
}

export function displayAllCourse (params) {
  return axios({
    url: '/system/search_course_all',
    method: 'get',
    params: params
  })
}

export function searchCourseByKeywordInDependency (params) {
  return axios({
    url: '/system/search_course_by_keyword_in_dependency',
    method: 'get',
    params: params
  })
}

export function searchCourseAllInDependency (params) {
  return axios({
    url: '/system/search_course_all_in_denpendency',
    method: 'get',
    params: params
  })
}

export function getStudentCourseList (params) {
  return axios({
    url: '/system/get_student_course_list',
    method: 'get',
    params: params
  })
}
