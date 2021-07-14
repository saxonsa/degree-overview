import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'
import storage from '../utils/storage'
import { notification } from 'ant-design-vue'
// import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  // ----------------------------------------------------------------- |
  /* User Logic */
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Account/Login.vue'),
    meta: {
      title: 'Login Page',
      isLogin: false
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Account/Register.vue'),
    meta: {
      title: 'Register Page',
      isLogin: false
    }
  },
  {
    path: '/reset_password',
    name: 'ResetPassword',
    component: () => import('../views/Account/ResetPassword.vue'),
    meta: {
      title: 'Reset password',
      isLogin: false
    }
  },
  // ----------------------------------------------------------------- |

  // ----------------------------------------------------------------- |
  // Dashboard
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: {
      title: 'dashboard',
      isLogin: true
      // requireAuth: true
    }
  },
  // ----------------------------------------------------------------- |

  // ----------------------------------------------------------------- |
  // course related
  {
    path: '/course_creation',
    name: 'CourseCreation',
    component: () => import('../views/course/CourseCreation.vue'),
    meta: {
      title: 'Course Creation',
      isLogin: true
    }
  },
  {
    path: '/course_detail/:courseCode/:courseName',
    name: 'CourseDetail',
    component: () => import('../views/course/CourseDetail.vue'),
    meta: {
      title: 'Course Detail',
      isLogin: true
    }
  },
  {
    path: '/depdendency_visualization',
    name: 'DependencyVisualization',
    component: () => import('../views/course/DependencyVisualization.vue'),
    meta: {
      title: 'Dependency Visualization',
      isLogin: true
    }
  },
  {
    path: '/all_course_for_student',
    name: 'AllCourseForStudent',
    component: () => import('../views/course/AllCourseForStudent.vue'),
    meta: {
      title: 'All Course For Student',
      isLogin: true
    }
  },
  // ----------------------------------------------------------------- |
  /* performance */
  {
    path: '/student_performance',
    name: 'StudentPerformance',
    component: () => import('../views/Grade/StudentPerformance.vue'),
    meta: {
      title: 'Student Performance',
      isLogin: true
    }
  },
  {
    path: '/course_analysis',
    name: 'CourseAnalysis',
    component: () => import('../views/Grade/CourseAnalysis.vue'),
    meta: {
      title: 'Course Analysis',
      isLogin: true
    }
  },

  // ----------------------------------------------------------------- |
  /* Error page */
  {
    path: '/error404',
    name: 'Error404',
    component: () => import('../views/ErrorPage/Error404.vue'),
    meta: {
      title: '404 error page'
    }
  },
  {
    path: '/error500',
    name: 'Error500',
    component: () => import('../views/ErrorPage/Error500.vue'),
    meta: {
      title: '500 error page'
    }
  },
  // 未找到页面时候跳转404
  {
    path: '*',
    redirect: '/error404'
  },
  // ----------------------------------------------------------------- |

  // ----------------------------------------------------------------- |
  // empty page
  {
    path: '/empty_page',
    name: 'EmptyPage',
    component: () => import('../views/emptyPage.vue'),
    meta: {
      title: 'empty page'
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(r => r.meta.isLogin)) {
    if (storage.get('JWT_TOKEN')) {
      store.commit('set_token', storage.get('JWT_TOKEN'))
      next()
    } else {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      notification.error({
        message: 'No Authorization detected',
        description: 'Please login first!'
      })
    }
  } else {
    next()
  }

  if (to.meta.title) {
    document.title = to.meta.title
  }
})

export default router
