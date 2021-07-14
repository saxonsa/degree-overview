import { axios } from '@/utils/request'

export function getAssessmentTemplate (params) {
  return axios({
    url: '/assessment/get_assessment_template',
    methods: 'get',
    params: params,
    responseType: 'blob'
  })
}
