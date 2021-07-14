import { axios } from '@/utils/request'

export function getStudentCILOScore (params) {
  return axios({
    url: '/grade/calculate_personal_cilo_score',
    methods: 'get',
    params: params
  })
}

export function getResultAnalysis (params) {
  return axios({
    url: '/grade/calculate_average_year_cilo_score_for_result_analysis',
    method: 'get',
    params: params
  })
}
