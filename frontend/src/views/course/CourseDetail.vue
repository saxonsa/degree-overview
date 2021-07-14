<template>
  <v-app id="inspire">
    <v-app-bar
      class="dashboard-app-bar"
      app
      flat
      dense
      min-height="20"
    >
      <a class="dashboard-nav-brand-title" @click="gotoDashboard">DegreeOverview</a>

      <v-btn-toggle
        borderless
        tile
        dense
        style="margin-left: 20px; font-size: 18px;"
        background-color="#ddd"
      >
        <v-menu
          offset-y
        >
          <!-- <template v-slot:activator="{attrs, on}">
            <v-btn
              class="nav-btn"
              value="user Guide"
              v-bind="attrs"
              v-on="on"
              tile
              plain
              depressed
            >
              <span class="hidden-sm-and-down nav-btn-text">User Guide</span>
              <v-icon class="vuetify-iconicon_down-arrow"></v-icon>
            </v-btn>
          </template> -->

          <v-list
            :outlined="true"
            tile
          >
            <v-list-item-group
              color="#33adfa"
            >
              <v-list-item
                class="menu-list-item"
                v-for="item in guide_items"
                :key="item"
                link
                dense
              >
                <v-list-item-title v-text="item"></v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>

        <!-- 创建课程按钮, 需要design权限 -->
        <v-btn
          v-if="parseInt(me.designAuth)"
          tile
          plain
          :depressed="true"
          class="nav-btn"
          @click="gotoCreateCourse"
        >
          <span class="hidden-sm-and-down nav-btn-text">Create course</span>
        </v-btn>

        <!-- Course visualization -->
        <v-btn
          tile
          plain
          :depressed="true"
          class="nav-btn"
          @click="gotoDependencyVisualization"
        >
          <span class="hidden-sm-and-down nav-btn-text">Visualize Dependency</span>
        </v-btn>

        <v-btn
          v-if="me.role=='student'"
          tile
          plain
          :depressed="true"
          class="nav-btn"
          @click="gotoAllCourse"
        >
          <span class="hidden-sm-and-down nav-btn-text">All Courses</span>
        </v-btn>
      </v-btn-toggle>

      <v-menu
        offset-y
        bottom
        max-width="150"
      >
        <template v-slot:activator="{attrs, on}">
          <v-btn
            value="Links"
            v-bind="attrs"
            v-on="on"
            tile
            plain
            depressed
            class="nav-btn hidden-sm-and-down ml-auto"
          >
            <v-avatar
              color="grey darken-1 shrink"
              size="32"
              v-bind="attrs"
              v-on="on"
            >
            </v-avatar>
            <span class="hidden-sm-and-down nav-btn-text" style="margin-left: 4%;">
              {{ me.engname? me.nickname + " (" + me.engname + ")" : me.nickname }}
            </span>
            <v-icon class="vuetify-iconicon_down-arrow"></v-icon>
          </v-btn>
        </template>

        <v-list
          :outlined="true"
          tile
        >
          <v-list-item-group
            color="#33adfa"
          >
            <v-list-item
              class="user-list-item"
              link
              dense
            >
              <v-list-item-title>
                <v-icon class="vuetify-icondashboard" small></v-icon>
                <span class="user-list-item-text">Dashboard</span>
              </v-list-item-title>
            </v-list-item>

            <v-divider></v-divider>

            <v-list-item
              class="user-list-item"
              link
              dense
            >
              <v-list-item-title>
                <v-icon class="vuetify-iconuser" small></v-icon>
                <span class="user-list-item-text">Profile</span>
              </v-list-item-title>
            </v-list-item>

            <v-list-item
              class="user-list-item"
              link
              dense
              v-if="me.role==='student'"
            >
              <v-list-item-title>
                <v-icon class="vuetify-icondengji" small></v-icon>
                <span class="user-list-item-text">Grade</span>
                </v-list-item-title>
            </v-list-item>

            <v-list-item
              class="user-list-item"
              link
              dense
            >
              <v-list-item-title>
                <v-icon class="vuetify-iconmessage" small></v-icon>
                <span class="user-list-item-text">Messages</span>
              </v-list-item-title>
            </v-list-item>

            <v-list-item
              class="user-list-item"
              link
              dense
            >
              <v-list-item-title>
                <v-icon class="vuetify-iconsettings" small></v-icon>
                <span class="user-list-item-text">Preferences</span>
                </v-list-item-title>
            </v-list-item>

            <v-divider></v-divider>

            <v-list-item
              class="user-list-item"
              link
              dense
              @click="logout"
            >
              <v-list-item-title>
                <v-icon class="vuetify-iconlog-out1" small></v-icon>
                <span class="user-list-item-text">logout</span>
              </v-list-item-title>
            </v-list-item>

          </v-list-item-group>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main class="white">
      <v-breadcrumbs :items="breadItems" large></v-breadcrumbs>
      <v-container>
        <v-row>
          <v-col
            cols="12"
            sm="3"
          >
            <!-- <a-card title="Course information changed history" >
              <a-timeline mode="left" style="text-align: left;" reverse>
                <a-timeline-item color="green">Create a services site 2015-09-01</a-timeline-item>
                <a-timeline-item>Solve initial network problems 2015-09-01</a-timeline-item>
                <a-timeline-item color="red">
                  <a-icon slot="dot" type="clock-circle-o" style="font-size: 16px;" />
                  Technical testing 2015-09-01
                </a-timeline-item>
                <a-timeline-item color="green">Create a services site 2015-09-01</a-timeline-item>
                <a-timeline-item>Solve initial network problems 2015-09-01</a-timeline-item>
                <a-timeline-item color="red">
                  Technical testing 2015-09-01
                </a-timeline-item>
                <a-timeline-item>Network problems being solved 2015-09-01</a-timeline-item>
                <a-timeline-item color="green">Create a services site 2015-09-01</a-timeline-item>
                <a-timeline-item>Solve initial network problems 2015-09-01</a-timeline-item>
                <a-timeline-item color="red">
                  <a-icon slot="dot" type="clock-circle-o" style="font-size: 16px;" />
                  Technical testing 2015-09-01
                </a-timeline-item>
                <a-timeline-item>
                    Network problems being solved 2015-09-01
                    <a-badge style="margin-left: 8px;" status="processing" slot="dot" />
                </a-timeline-item>
              </a-timeline>
            </a-card> -->
            <v-sheet
              class="white"
              min-height="268"
            >

            </v-sheet>
          </v-col>

          <v-col
            cols="12"
            sm="9"
          >
            <v-sheet
              class="white"
              min-height="85vh"
            >
              <v-container>
                <v-row>
                  <v-btn
                    v-if="me.role=='designer'&&!editMode"
                    color="blue darken-3"
                    dark
                    class="lower-letter-btn"
                    @click="openEditMode"
                  >
                    <v-icon style="margin-right: 5px;">mdi-square-edit-outline</v-icon>
                    Edit
                  </v-btn>
                  <v-btn
                    v-if="editMode"
                    color="green darken-3"
                    dark
                    class="lower-letter-btn"
                    @click="saveEditInfo"
                  >
                    <v-icon style="margin-right: 5px;">mdi-sticker-check-outline</v-icon>
                    Save
                  </v-btn>
                </v-row>
              </v-container>
              <a-spin tip="Loading course detail..." :spinning="detailSpin">
                <a-descriptions title="Course Basic Information" bordered>
                  <a-descriptions-item label="Course Name" :span="3">
                    <span>{{ course.name }}</span>
                  </a-descriptions-item>
                  <a-descriptions-item label="Course Code">
                    <span>{{ course.code }}</span>
                  </a-descriptions-item>
                  <a-descriptions-item label="Course Type">
                    <span v-if="!editMode">{{ course.type }}</span>
                    <el-input
                      placeholder="Course Type"
                      v-if="editMode"
                      v-model="course.type"
                      clearable>
                    </el-input>
                  </a-descriptions-item>
                  <a-descriptions-item label="Course Unit">
                    <span v-if="!editMode">{{ course.unit }}</span>
                    <el-input
                      placeholder="Course Unit"
                      v-if="editMode"
                      v-model="course.unit"
                      clearable>
                    </el-input>
                  </a-descriptions-item>
                  <a-descriptions-item label="Program" :span="2">
                    <span>{{ course.department }}</span>
                  </a-descriptions-item>
                  <a-descriptions-item label="Start year for assessment">
                    <span v-if="!editMode">{{ course.academic_year }}</span>
                    <el-date-picker
                      v-if="editMode"
                      v-model="course.academic_year"
                      type="year"
                      placeholder="choose year"
                      value-format="yyyy">
                    </el-date-picker>
                  </a-descriptions-item>
                  <a-descriptions-item label="CILO" :span="3">
                    <v-row v-for="(cilo, key) in course.CILO" :key="key">
                      <v-col v-if="!editMode" cols="12" md="2" style="text-align: center;">CILO {{ cilo.index }}: </v-col>
                      <v-col v-if="!editMode" md="9" style="text-align: left;">{{ cilo.content }}</v-col>
                      <v-col v-if="editMode" cols="12" md="2" style="text-align: center; margin-top: 10px;">CILO {{ cilo.index }}: </v-col>
                      <v-col v-if="editMode" md="6">
                        <el-input
                          placeholder="CILO Content"
                          v-if="editMode"
                          v-model="cilo.content"
                          clearable>
                        </el-input>
                      </v-col>
                    </v-row>
                  </a-descriptions-item>
                  <a-descriptions-item label="Assessment" :span="3">
                    <v-row v-if="editMode">
                      <v-btn
                        style="margin-left: 15px; margin-top: 20px;"
                        color="teal darken-4"
                        dark
                        @click="addAssessment"
                      >
                        <v-icon dark>
                          mdi-pencil-plus-outline
                        </v-icon>
                        <span
                          style="margin-top: 3px; margin-left: 5px;"
                          class="lower-letter-btn">Add Assessment
                        </span>
                      </v-btn>
                    </v-row>
                    <v-row v-for="(assessment, key) in course.assessment" :key="key">
                      <v-col cols="12" md="3" style="text-align: left;">
                        <span v-if="!editMode">Method{{ key + 1 }}: {{ assessment.method }}</span>
                        <span v-if="editMode">Method{{ key + 1 }}:
                          <el-input
                            placeholder="Method"
                            v-model="assessment.method"
                            clearable>
                          </el-input>
                        </span>
                      </v-col>
                      <v-col md="2" style="text-align: left;">
                        <span v-if="!editMode"> Weight: {{ assessment.weight * 100 }}%</span>
                        <span v-if="editMode">Weight:
                          <el-input
                            placeholder="Weight"
                            v-model="assessment.weight"
                            clearable
                          ></el-input>
                        </span>
                      </v-col>
                      <v-col md="5" style="text-align: left;">
                        <span v-if="!editMode"> Corresponding CILO: <strong>{{ assessment.cilostr }}</strong></span>
                        <span v-if="editMode">Corresponding CILO:
                          <el-input
                            placeholder="correspoding CILO"
                            v-model="assessment.cilostr"
                            clearable
                          ></el-input>
                        </span>
                      </v-col>
                      <v-col md="2" v-if="editMode" style="margin-top: 20px;">
                        <v-btn
                          color="red darken-4"
                          dark
                          @click="deleteAssessment(key)"
                        >
                          <v-icon dark>
                            mdi-delete
                          </v-icon>
                          delete
                        </v-btn>
                      </v-col>
                    </v-row>
                  </a-descriptions-item>
                  <a-descriptions-item v-if="!editMode && course.prerequisite_course.length" label="Prerequisite course list" :span="3">
                    <v-row v-for="(preCourse, key) in course.prerequisite_course" :key="key">
                      <v-col cols="12" md="12">
                        <a style="color: green" @click="gotoPrerequisiteCourse(preCourse.code)">{{ preCourse.code }} ({{ preCourse.type }}) {{ preCourse.name }}</a>
                      </v-col>
                    </v-row>
                  </a-descriptions-item>
                  <a-descriptions-item v-if="!editMode && !course.prerequisite_course.length" label="Prerequisite course" :span="3">
                    <span>None</span>
                  </a-descriptions-item>
                  <a-descriptions-item v-if="!editMode && course.post_courses.length" label="Post course list" :span="3">
                    <v-row v-for="(postCourse) in course.post_courses" :key="postCourse.code">
                      <v-col cols="12" md="12">
                        <a style="color: blue" @click="gotoPostCourse(postCourse.code)">{{ postCourse.code }} ({{ postCourse.type }}) {{ postCourse.name }}</a>
                      </v-col>
                    </v-row>
                  </a-descriptions-item>
                  <a-descriptions-item v-if="!editMode && !course.post_courses.length" label="Post course list" :span="3">
                    <span>None</span>
                  </a-descriptions-item>
                </a-descriptions>

                <br/>
                <v-container v-if="!editMode">
                  <h5 v-if="!editMode && course.prerequisite_course.length">Prerequisite CILO Relation</h5>
                  <a-descriptions bordered v-for="(preRelation, key) in course.prerequisite_relation" :key="key">
                    <a-descriptions-item label="Current CILO Index" :span="1" >
                      {{ preRelation.current_cilo_index }}
                    </a-descriptions-item>
                    <a-descriptions-item label="Post Course" :span="1">
                      <a style="color: green;" @click="gotoPrerequisiteCourse(preRelation.pre_course_code)">{{ preRelation.pre_course_code }}</a>
                    </a-descriptions-item>
                    <a-descriptions-item label="Post CILO Index" :span="1">
                      {{ preRelation.pre_cilo_index }}
                    </a-descriptions-item>
                  </a-descriptions>

                  <br/>
                  <h5 v-if="course.post_courses.length">Post CILO Relation (Courses use current course as prerequisite)</h5>
                  <a-descriptions bordered v-for="(postRelation) in course.post_relation" :key="postRelation.post_course_code + postRelation.post_cilo_index + postRelation.pre_cilo_index">
                    <a-descriptions-item label="Current CILO Index" :span="1" >
                      {{ postRelation.pre_cilo_index }}
                    </a-descriptions-item>
                    <a-descriptions-item label="Post Course" :span="1">
                      <a style="color: blue;" @click="gotoPostCourse(postRelation.post_course_code)">{{ postRelation.post_course_code }}</a>
                    </a-descriptions-item>
                    <a-descriptions-item label="Post CILO Index" :span="1">
                      {{ postRelation.post_cilo_index }}
                    </a-descriptions-item>
                  </a-descriptions>
                </v-container>
              </a-spin>
            </v-sheet>
          </v-col>

          <!-- <v-col
            cols="12"
            sm="2"
          >
            <v-sheet
              class="grey lighten-3"
              min-height="100"
            >
            </v-sheet>
          </v-col> -->
        </v-row>
      </v-container>
    </v-main>
    <v-footer
      dark
      padless
    >
      <v-card
        class="flex"
        flat
        tile
      >
        <v-card-text class="py-2 white--text text-center">
          <span>Copyright &copy;{{ new Date().getFullYear() }} <strong>Daffodil</strong> All Rights Reserved</span>
        </v-card-text>
      </v-card>
    </v-footer>
    <router-view :key="$route.fullPath"></router-view>
  </v-app>
</template>
<script>
import { mapState } from 'vuex'
import { getCourseDetailByCourseCode, modifyCourse } from '@/api/course'
export default {
  name: 'CourseDetail',
  data: () => ({
    guide_items: [
      'User Guide for Student',
      'User Guide for Lecturers',
      'User Guide for Course designer'
    ],
    breadItems: [
      {
        text: 'Dashboard',
        disabled: false,
        href: '/'
      },
      {
        text: 'Course Name',
        disabled: true
      }
    ],

    course: {
      code: '',
      name: '',
      type: '',
      unit: 0,
      department: '',
      academic_year: '',
      CILO: [],
      assessment: [],

      // Time: 2021/5/15
      // 修复warning, 每次template优先渲染这个course变量, 其中并没有prerequisite_course
      // 所以会报undefined
      // 解决办法: 在course这里优先初始化一下
      prerequisite_course: [],
      post_relation: [],
      post_courses: []
      // datePickerPanelOpen: false
    },

    detailSpin: false,
    editMode: false
  }),
  computed: {
    ...mapState({
      me: state => state.me
    })
  },
  created () {
    this.course.code = this.$route.params.courseCode
    this.course.name = this.$route.params.courseName
    this.breadItems[1].text = this.course.code + ' ' + this.course.name
  },
  mounted () {
    this.detailSpin = true
    getCourseDetailByCourseCode({
      courseCode: this.$route.params.courseCode
    }).then(res => {
      this.course = res.result
      this.detailSpin = false
    })
  },
  methods: {
    logout: function () {
      // logout 时删除 token
      this.$store.commit('del_token')
      this.$router.push({ name: 'Login' })
    },
    gotoDashboard: function () {
      this.$router.push({ name: 'Dashboard' })
    },
    gotoCreateCourse: function () {
      // 跳转创建课程界面
      if (parseInt(this.me.designAuth) === 1) {
        // 有权限就跳转
        this.$router.push({ name: 'CourseCreation' })
      } else {
        // 如果没有权限, 显示 alert
        this.$store.dispatch('openSnackBar', {
          msg: 'No authorization to create course',
          color: '#FFD54F',
          closeBtnColor: '#FFCC80',
          visible: true
        })
      }
    },
    gotoDependencyVisualization () {
      this.$router.push({ name: 'DependencyVisualization' })
    },
    gotoAllCourse: function () {
      this.$router.push({ name: 'AllCourseForStudent' })
    },
    gotoPrerequisiteCourse (courseCode) {
      // 点击跳转前置课程信息界面
      var courseName = ''
      for (var i = 0; i < this.course.prerequisite_course.length; i++) {
        if (this.course.prerequisite_course[i].code === courseCode) {
          courseName = this.course.prerequisite_course[i].name
          break
        }
      }
      this.$router.push({ name: 'CourseDetail', params: { courseCode: courseCode, courseName: courseName } })
    },
    gotoPostCourse (courseCode) {
      // 点击跳转后置课程信息界面
      var courseName = ''
      for (var i = 0; i < this.course.post_courses.length; i++) {
        if (this.course.post_courses[i].code === courseCode) {
          courseName = this.course.post_courses[i].name
          break
        }
      }
      this.$router.push({ name: 'CourseDetail', params: { courseCode: courseCode, courseName: courseName } })
    },
    openEditMode () {
      this.editMode = true
      this.$Message.info('Edit mode is on!')
    },
    addAssessment () {
      this.course.assessment.push({
        method: '',
        weight: 0.0,
        cilostr: '',
        year: ''
      })
    },
    deleteAssessment (index) {
      this.course.assessment.splice(index, 1)
    },
    saveEditInfo () {
      // 保存修改
      // validate information changed
      // 1. Basic Information
      if (!this.course.type) {
        this.$Message.error('Course type cannot be empty!')
        return
      }
      if (!this.course.unit) {
        this.$Message.error('Course unit cannot be empty!')
        return
      } else {
        if (!(this.course.unit instanceof Number)) {
          // 用正则判断 course unit 是不是数字
          var integer = /^\d+$/ // 正整数
          var realNumberNotStartFrom0 = /^[1-9]\d*[.]\d+$/ // 不是0开头的实数
          var realNumberStartFrom0 = /^0[.]\d+$/ // 0开头的实数
          if (integer.test(this.course.unit) || realNumberNotStartFrom0.test(this.course.unit) || realNumberStartFrom0.test(this.course.unit)) {
            this.course.unit = Number(this.course.unit)
          } else {
            this.$Message.error('Course unit must be a non-negative number')
            return
          }
        }
      }
      if (!this.course.academic_year) {
        this.$Message.error('Empty academic year detected!')
        return
      }

      // 2. CILO
      var i = 0
      for (i = 0; i < this.course.CILO.length; i++) {
        if (this.course.CILO[i].content === '') {
          this.$Message.error('The content of CILO' + this.course.CILO[i].index + ' cannot be empty!')
          return
        }
      }

      // 3. Assessment
      // 3.1 empty test
      var totalWeight = 0
      const maxCILO = this.course.CILO.length
      for (i = 0; i < this.course.assessment.length; i++) {
        if (this.course.assessment[i].method === '') {
          this.$Message.error('The method field cannot be empty!')
          return
        }
        if (this.course.assessment[i].weight === '') {
          this.$Message.error('The weight field cannot be empty!')
          return
        } else {
          // 修改后的weight不是数字, 如果改了weight, 需要将其转化为数字格式
          if (!(this.course.assessment[i].weight instanceof Number)) {
            this.course.assessment[i].weight = Number(this.course.assessment[i].weight)
            // 3.2检测weight是不是0
          }
          if (this.course.assessment[i].weight === 0) {
            this.$Message.error('Weight cannot be 0')
            return
          }
          totalWeight += this.course.assessment[i].weight
        }
        if (this.course.assessment[i].cilostr === '') {
          this.$Message.error('The corresponding CILO feild cannot be empty!')
          return
        } else {
          // 3.3 检测assessment corresponding CILO的格式
          var CILOFormat = /^\d(-\d)*$/
          if (!(CILOFormat.test(this.course.assessment[i].cilostr))) {
            this.$Message.error('The corresponding CILO must follow the format like "1-2-3"!')
            return
          }
          const correspondingCILOList = this.course.assessment[i].cilostr.split('-') // 将cilostr转换为数组
          const sortedCILOList = correspondingCILOList.sort()
          for (var j = 0; j < correspondingCILOList.length; j++) {
            // 3.4 检测corresponding CILO是不是填写了存在的CILO
            if (sortedCILOList[j] > maxCILO || sortedCILOList[j] < 1) {
              this.$Message.error('Non-existed CILO used in corresponding CILO')
              return
            }
            // 3.5 检测一个method中的corresponding CILO有没有重复
            if (j !== 0 && sortedCILOList[j] === sortedCILOList[j - 1]) {
              this.$Message.error('Duplicated corresponding CILOs in one method are detected!')
              return
            }
          }
        }
      }

      // 3.6 validate total weight
      if (Number(totalWeight.toFixed(2)) !== 1) {
        this.$Message.error('Total weight does not equal to 1, please check each weight feild!')
        return
      }

      // 修改课程
      this.$Message.loading('modifying...')
      modifyCourse({
        staffid: this.me.id,
        courseCode: this.course.code,
        courseName: this.course.name,
        courseType: this.course.type,
        courseUnit: this.course.unit,
        courseDepartment: this.course.department,
        courseAcademicYear: this.course.academic_year,
        courseCILO: this.course.CILO,
        courseAssessment: this.course.assessment
      }).then(res => {
        console.log(res)
        if (res.code === 200) {
          this.$Message.success(res.info)
          this.editMode = false
        }
      }).catch(error => {
        console.log('oops! error detected!')
        console.err(error)
      })
    }
  }
}
</script>

<style scoped>
  .dashboard-app-bar {
    background: linear-gradient(white, #BDBDBD);
  }
  .dashboard-nav-brand-title {
    font-size: 20px;
    font-weight: 300;
  }
  .nav-btn {
    text-transform: capitalize;
    background: linear-gradient(white, #BDBDBF);
    height: 100%;
  }
  .nav-btn-text {
    font-size: 16px;
    color: black;
  }
  .menu-list-item {
    text-align: left;
  }
  .user-list-item {
    text-align: left;
  }
  .user-list-item-text {
    margin-left: 10px;
  }
  .dashboard-title {
    font-size: 18px;
  }
  .v-list-item--dense, .v-list--dense .v-list-item {
    min-height: 30px;
  }

  .lower-letter-btn {
    text-transform: none;
  }
</style>
