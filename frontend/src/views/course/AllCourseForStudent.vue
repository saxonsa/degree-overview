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
          disabled
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
            sm="2"
          >
            <v-sheet
              class="white"
              min-height="268"
            >
              <!--  -->
            </v-sheet>
          </v-col>

          <v-col
            cols="15"
            sm="8"
          >
            <v-sheet
              class="grey lighten-3"
              min-height="85vh"
            >
              <v-container></v-container> <!-- 占位DOM, 之后要优化一下这里 -->
              <v-text-field
                solo
                clearable
                flat
                dense
                v-model="searchValue"
                placeholder="search course..."
                prepend-inner-icon="vuetify-iconsearch"
                style="margin-right: 15px;"
              >

                <v-select
                  v-model="searchType"
                  style="margin-left: 20px; bottom: 6px;"
                  slot="prepend"
                  :items="searchItems"
                  label="Search Type"
                  dense
                  outlined
                  item-color="teal darken-2"
                ></v-select>

                <v-btn slot="append" tile style="left: 12px;" @click="searchCourse">
                  <v-icon class="vuetify-icongo"></v-icon>
                  <span style="margin-left: 10px;">Enter</span>
                </v-btn>
              </v-text-field>

              <v-alert v-if="alert" dense text type="info">{{alertMsg}}</v-alert>

              <a-spin tip="Loading" :spinning="courseListSpin">
                <v-container v-if="resultType == 'by CILO' || resultType == 'by keyword'">
                  <a-table :columns="CILOColumns" :data-source="CILOData" />
                </v-container>
                <v-container v-if="resultType == 'by Course'">
                  <v-expansion-panels
                    v-for="(item, key) in courseGroup"
                    :key="key"
                  >
                    <v-alert v-if="key>0" dense text type="info" style="margin-top: 10px;">Course group divider</v-alert>
                    <v-expansion-panel
                      style="margin-top: 1px;"
                      v-model="panel"
                    >
                      <v-expansion-panel-header>
                        <span style="font-size: 14px;">
                          <a-tag color="blue">Current</a-tag>
                          {{ item.current.code }}
                          ({{ item.current.type }})
                          {{ item.current.name }}
                        </span>
                      </v-expansion-panel-header>

                      <v-expansion-panel-content style="margin-top: 20px; margin-left: 12px;">
                        <!-- 显示CILO -->
                        <v-row v-if="item.current.CILO[0]">
                          <span style="margin-top: 15px; margin-left: 14px; margin-bottom: 15px;"> CILO:  </span>
                          <br/>
                        </v-row>

                        <v-row
                          no-gutters
                          v-for="(cilo, key) in item.current.CILO"
                          :key="key">
                          <v-col cols="2">
                            <span>CILO{{key + 1}}: </span>
                          </v-col>
                          <v-spacer></v-spacer>
                          <v-col cols="10">
                            <!-- 自动换行 -->
                            <span class="expansion-content">
                              {{ cilo }}
                            </span>
                          </v-col>
                        </v-row>

                        <v-divider></v-divider>

                        <v-btn
                          v-if="me.role=='student'"
                          small
                          depressed
                          class="lower-letter-btn white--text"
                          color="blue darken-3"
                          @click="gotoStudentPerformance(item.current.code, item.current.name)"
                        >Course Performance
                        </v-btn>
                        <v-btn
                          v-else
                          small
                          depressed
                          class="lower-letter-btn white--text"
                          color="blue darken-3"
                          @click="gotoCourseAnalysis(item.current.code, item.current.name)"
                        >Analysis Results
                        </v-btn>
                        <v-btn
                          small
                          depressed
                          class="lower-letter-btn white--text"
                          color="teal darken-3"
                          style="margin-left: 20px;"
                          @click="gotoCourseDetail(item.current.code, item.current.name)"
                        >Course Detail
                        </v-btn>

                      </v-expansion-panel-content>

                    </v-expansion-panel>
                    <v-expansion-panels v-if="item.pre[0]">
                      <v-expansion-panel
                        style="margin-top: 1px;"
                        v-for="(pre, key) in item.pre"
                        :key="key"
                        v-model="panel"
                      >
                        <v-expansion-panel-header>
                          <span style="font-size: 14px;">
                            <a-tag color="pink">pre</a-tag>
                            {{ pre.code }}
                            ({{ pre.type }})
                            {{ pre.name }}
                          </span>
                        </v-expansion-panel-header>

                        <v-expansion-panel-content style="margin-top: 20px; margin-left: 12px;">
                          <!-- 显示CILO -->
                          <v-row v-if="pre.CILO[0]">
                            <span style="margin-top: 15px; margin-left: 14px; margin-bottom: 15px;"> CILO:  </span>
                            <br/>
                          </v-row>

                          <v-row
                            no-gutters
                            v-for="(pre_cilo, pre_key) in pre.CILO"
                            :key="pre_key">
                            <v-col cols="2">
                              <span>CILO{{pre_key + 1}}: </span>
                            </v-col>
                            <v-spacer></v-spacer>
                            <v-col cols="10">
                              <!-- 自动换行 -->
                              <span class="expansion-content">
                                {{ pre_cilo }}
                              </span>
                            </v-col>
                          </v-row>

                          <v-divider></v-divider>

                          <v-btn
                            v-if="me.role=='student'"
                            small
                            depressed
                            class="lower-letter-btn white--text"
                            color="blue darken-3"
                            @click="gotoStudentPerformance(pre.code, pre.name)"
                          >Course Performance
                          </v-btn>
                          <v-btn
                            v-else
                            small
                            depressed
                            class="lower-letter-btn white--text"
                            color="blue darken-3"
                            @click="gotoCourseAnalysis(pre.code, pre.name)"
                          >Analysis Results
                          </v-btn>
                          <v-btn
                            small
                            depressed
                            class="lower-letter-btn white--text"
                            color="teal darken-3"
                            style="margin-left: 20px;"
                            @click="gotoCourseDetail(pre.code, pre.name)"
                          >Course Detail
                          </v-btn>

                        </v-expansion-panel-content>

                      </v-expansion-panel>
                    </v-expansion-panels>
                    <v-expansion-panels v-if="item.post[0]">
                      <v-expansion-panel
                        style="margin-top: 1px;"
                        v-for="(post, key) in item.post"
                        :key="key"
                        v-model="panel"
                      >
                        <v-expansion-panel-header>
                          <span style="font-size: 14px;">
                            <a-tag color="green">post</a-tag>
                            {{ post.code }}
                            ({{ post.type }})
                            {{ post.name }}
                          </span>
                        </v-expansion-panel-header>

                        <v-expansion-panel-content style="margin-top: 20px; margin-left: 12px;">
                          <!-- 显示CILO -->
                          <v-row v-if="post.CILO[0]">
                            <span style="margin-top: 15px; margin-left: 14px; margin-bottom: 15px;"> CILO:  </span>
                            <br/>
                          </v-row>

                          <v-row
                            no-gutters
                            v-for="(post_cilo, post_key) in post.CILO"
                            :key="post_key">
                            <v-col cols="2">
                              <span>CILO{{post_key + 1}}: </span>
                            </v-col>
                            <v-spacer></v-spacer>
                            <v-col cols="10">
                              <!-- 自动换行 -->
                              <span class="expansion-content">
                                {{ post_cilo }}
                              </span>
                            </v-col>
                          </v-row>

                          <v-divider></v-divider>

                          <v-btn
                            v-if="me.role=='student'"
                            small
                            depressed
                            class="lower-letter-btn white--text"
                            color="blue darken-3"
                            @click="gotoStudentPerformance(post.code, post.name)"
                          >Course Performance
                          </v-btn>
                          <v-btn
                            v-else
                            small
                            depressed
                            class="lower-letter-btn white--text"
                            color="blue darken-3"
                            @click="gotoCourseAnalysis(post.code, post.name)"
                          >Analysis Results
                          </v-btn>
                          <v-btn
                            small
                            depressed
                            class="lower-letter-btn white--text"
                            color="teal darken-3"
                            style="margin-left: 20px;"
                            @click="gotoCourseDetail(post.code, post.name)"
                          >Course Detail
                          </v-btn>

                        </v-expansion-panel-content>

                      </v-expansion-panel>
                    </v-expansion-panels>
                  </v-expansion-panels>
                </v-container>

                <v-expansion-panels v-model="panel" v-if="resultType != 'by Course' && resultType != 'by CILO'">
                  <v-expansion-panel
                    v-for="(item, key) in courses"
                    :key="key"
                  >
                    <v-expansion-panel-header>
                      <span style="font-size: 14px;">
                        {{ item.course_code }}
                        ({{ item.course_type }})
                        {{item.course_name}}
                      </span>
                    </v-expansion-panel-header>
                    <v-expansion-panel-content style="margin-top: 20px; margin-left: 12px;">

                      <!-- 显示CILO -->
                      <v-row v-if="item.cilo[0]">
                        <span style="margin-top: 15px; margin-left: 14px; margin-bottom: 15px;"> CILO:  </span>
                        <br/>
                      </v-row>

                      <v-row
                        no-gutters
                        v-for="(cilo, key) in item.cilo"
                        :key="key">
                        <v-col cols="2">
                          <span>CILO{{cilo.cilo_index}}: </span>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col cols="10">
                          <!-- 自动换行 -->
                          <span class="expansion-content">
                            {{cilo.cilo_content}}
                          </span>
                        </v-col>
                      </v-row>

                      <v-divider v-if="item.prerequisite_course[0]"></v-divider>
                      <v-row v-if="item.prerequisite_course[0]">
                        <span style="margin-top: 15px; margin-left: 14px; margin-bottom: 20px;"> Prerequisite Course:  </span>
                        <br/>
                      </v-row>

                      <!-- 显示前置课程 -->
                      <v-row
                        no-gutters
                        v-for="(prerequisite, key) in item.prerequisite_course"
                        :key="prerequisite.course_code"
                      >
                        <v-col cols="4">
                          <span class="expansion-content" style="margin-left: 15%;">prerequisite course {{ key + 1 }}: </span>
                        </v-col>
                        <v-spacer></v-spacer>
                        <v-col cols="8">
                          <span class="expansion-content">
                            {{ prerequisite.course_code }} ({{ prerequisite.course_type }}) {{ prerequisite.course_name }}
                          </span>
                        </v-col>
                      </v-row>

                      <v-divider></v-divider>

                      <v-btn
                        small
                        depressed
                        class="lower-letter-btn white--text"
                        color="teal darken-3"
                        style="margin-left: 20px;"
                        @click="gotoCourseDetail(item.course_code, item.course_name)"
                      >Course Detail
                      </v-btn>

                    </v-expansion-panel-content>
                  </v-expansion-panel>
                </v-expansion-panels>
              </a-spin>
              <v-pagination
                v-if="courses[0] && resultType != 'by course (with code)'"
                v-model="page"
                :length="total_page"
                total-visible="10"
                prev-icon="mdi-menu-left"
                next-icon="mdi-menu-right"
                color="blue darken-3"
                style="margin-top: 30px;"
              ></v-pagination>

            </v-sheet>
          </v-col>

          <v-col
            cols="12"
            sm="2"
          >
            <v-sheet
              class="white"
              min-height="100"
            >
              <!--  -->
            </v-sheet>
          </v-col>
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
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
import { searchCourseByTypeAndKeyword, displayAllCourse } from '@/api/system.js'
import storage from '@/utils/storage.js'
export default {
  name: 'AllCourseForStudent',
  data: () => ({
    breadItems: [
      {
        text: 'Dashboard',
        disabled: false,
        href: '/'
      }
    ],
    guide_items: [
      'User Guide for Student',
      'User Guide for Lecturers',
      'User Guide for Course designer'
    ],
    link_items: [
      'UIC Home',
      'MIS',
      'Panopto',
      'Mahara',
      'Learning Resource Center',
      'Student Performance (PD only)'
    ],
    searchItems: [
      'by Course',
      'by CILO',
      'by keyword'
    ],
    searchType: 'by name',
    searchValue: '',
    resultType: 'all',

    prerequisite_course: [],
    courses: {}, // 课程列表
    page: 1, // 当前页码
    total_page: 1, // 总页码

    // 用于解决bug: 当页码为2的时候如果搜索后其实只有1页，那么会什么都显示不出来
    // 思路: 记录之前的状态, 将现在的状态和之前的进行比较:
    //      - 如果改变了, 那么将page置为1
    //      - 如果没有改变, 继续使用当前的page
    previousSearchState: {
      previousType: 'by name',
      previsouValue: ''
    },

    // 用于解决bug: 当打开折叠面板后, 切换了页码还仍然打开新页面对应的折叠面板
    // 思路: panel 可以检测到已经折叠面板是否打开
    //        - 如果折叠面板处于打开状态: panel 为对应打开的index
    //        - 如果折叠面板未打开: panel 为undefined
    // 那么可以在切换也页面后, 将panel设为undefined, 即关闭了折叠面板
    panel: '',

    courseListSpin: false,

    Loading: null,

    // 课程上方提示信息
    alertMsg: '',
    alert: false,

    courseGroup: [],
    CILOGroup: [],
    CILOColumns: [],
    CILOData: []
  }),

  computed: {
    ...mapState({
      me: state => state.me
    })
  },
  created () {
    this.searchCourse()

    // 回车快捷键绑定 搜索课程事件 searchCourse()
    const that = this
    document.onkeydown = function (e) {
      e = window.event || e
      if (that.$route.path === '/' && (e.code === 'Enter' || e.code === 'enter')) {
        that.searchCourse()
      }
    }
  },
  watch: {
    page () {
      this.searchCourse()
    },
    resultType () {
      console.log(this.resultType)
    }
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
    gotoCourseDetail: function (courseCode, courseName) {
      // 跳转课程信息界面
      this.$router.push({ name: 'CourseDetail', params: { courseCode: courseCode, courseName: courseName } })
    },
    gotoDependencyVisualization: function () {
      this.$router.push({ name: 'DependencyVisualization' })
    },
    gotoStudentPerformance: function (courseCode, courseName) {
      // 跳转学生performance界面
      storage.remove('courseCode')
      storage.remove('courseName')
      this.$router.push({ name: 'StudentPerformance', params: { courseCode: courseCode, courseName: courseName } })
    },
    gotoCourseAnalysis: function (courseCode, courseName) {
      // 跳转course analysis界面
      storage.remove('courseCode')
      storage.remove('courseName')
      this.$router.push({ name: 'CourseAnalysis', params: { courseCode: courseCode, courseName: courseName } })
    },
    searchCourse: function () {
      this.courseListSpin = true // 刚开始搜索时打开加载动画

      if (this.searchValue !== this.previousSearchState.previsouValue ||
        this.searchType !== this.previousSearchState.previousType) {
        this.page = 1
        this.previousSearchState.previsouValue = this.searchValue
        this.previousSearchState.previousType = this.searchType
      }
      if (this.searchValue && this.searchType) {
        searchCourseByTypeAndKeyword({
          page: this.page,
          type: this.searchType,
          keyword: this.searchValue
        }).then(res => {
          if (res.search_type === 'by Course') {
            this.courseGroup = res.result
            this.total_page = res.total_page
            this.resultType = res.search_type
            console.log(this.courseGroup)
          } else if (res.search_type === 'by CILO') {
            this.resultType = res.search_type
            this.CILOGroup = res.result
            this.total_page = 1

            this.CILOColumns = [
              {
                title: 'Course code',
                dataIndex: 'courseCode'
              },
              {
                title: 'CILO Content',
                dataIndex: 'CILOContent'
              },
              {
                title: 'related course',
                dataIndex: 'relatedCourse'
              },
              {
                title: 'related CILO',
                dataIndex: 'relatedCILO'
              },
              {
                title: 'relation',
                dataIndex: 'relation'
              }
            ]
            this.CILOData = []
            for (var i = 0; i < this.CILOGroup.length; i++) {
              // 添加前置关系
              for (var k = 0; k < this.CILOGroup[i].pre.length; k++) {
                this.CILOData.push({
                  key: this.CILOGroup[i].current.course.code + ' ' + this.CILOGroup[i].current.cilo_content + ' ' + this.CILOGroup[i].pre[k].course.code + ' ' + this.CILOGroup[i].pre[k].cilo_content,
                  courseCode: this.CILOGroup[i].current.course.code,
                  CILOContent: this.CILOGroup[i].current.cilo_content,
                  relatedCourse: this.CILOGroup[i].pre[k].course.code,
                  relatedCILO: this.CILOGroup[i].pre[k].cilo_content,
                  relation: 'pre'
                })
              }

              // 添加后置关系
              for (var j = 0; j < this.CILOGroup[i].post.length; j++) {
                this.CILOData.push({
                  key: this.CILOGroup[i].current.course.code + ' ' + this.CILOGroup[i].current.cilo_content + ' ' + this.CILOGroup[i].post[j].course.code + ' ' + this.CILOGroup[i].post[j].cilo_content,
                  courseCode: this.CILOGroup[i].current.course.code,
                  CILOContent: this.CILOGroup[i].current.cilo_content,
                  relatedCourse: this.CILOGroup[i].post[j].course.code,
                  relatedCILO: this.CILOGroup[i].post[j].cilo_content,
                  relation: 'post'
                })
              }
            }
            console.log(this.CILOGroup)
          } else if (res.search_type === 'by keyword') {
            this.CILOGroup = []
            this.CILOData = []
            this.resultType = res.search_type
            this.CILOGroup = res.result.cilo
            this.total_page = 1

            this.courses = res.result.course
            // this.courseGroup = res.result.course

            this.CILOColumns = [
              {
                title: 'Course code',
                dataIndex: 'courseCode'
              },
              {
                title: 'CILO Content',
                dataIndex: 'CILOContent'
              },
              {
                title: 'related course',
                dataIndex: 'relatedCourse'
              },
              {
                title: 'related CILO',
                dataIndex: 'relatedCILO'
              },
              {
                title: 'relation',
                dataIndex: 'relation'
              }
            ]
            this.CILOData = []
            for (i = 0; i < this.CILOGroup.length; i++) {
              // 添加前置关系
              for (k = 0; k < this.CILOGroup[i].pre.length; k++) {
                this.CILOData.push({
                  key: this.CILOGroup[i].current.course.code + ' ' + this.CILOGroup[i].current.cilo_content + ' ' + this.CILOGroup[i].pre[k].course.code + ' ' + this.CILOGroup[i].pre[k].cilo_content,
                  courseCode: this.CILOGroup[i].current.course.code,
                  CILOContent: this.CILOGroup[i].current.cilo_content,
                  relatedCourse: this.CILOGroup[i].pre[k].course.code,
                  relatedCILO: this.CILOGroup[i].pre[k].cilo_content,
                  relation: 'pre'
                })
              }

              // 添加后置关系
              for (j = 0; j < this.CILOGroup[i].post.length; j++) {
                this.CILOData.push({
                  key: this.CILOGroup[i].current.course.code + ' ' + this.CILOGroup[i].current.cilo_content + ' ' + this.CILOGroup[i].post[j].course.code + ' ' + this.CILOGroup[i].post[j].cilo_content,
                  courseCode: this.CILOGroup[i].current.course.code,
                  CILOContent: this.CILOGroup[i].current.cilo_content,
                  relatedCourse: this.CILOGroup[i].post[j].course.code,
                  relatedCILO: this.CILOGroup[i].post[j].cilo_content,
                  relation: 'post'
                })
              }
            }
          }
          this.courseListSpin = false
        })
        // searchCourseByTypeAndKeyword({
        //   page: this.page,
        //   type: this.searchType,
        //   keyword: this.searchValue
        // }).then(res => {
        //   if (this.searchType === 'by Course') {
        //     console.log('here')
        //   }
        //   this.courses = res.result.course
        //   this.total_page = res.result.total_page
        //   this.resultType = res.result.search_type

        //   // 搜到结果后关闭搜索动画
        //   this.courseListSpin = false
        // })
      } else {
        displayAllCourse({
          page: this.page
        }).then(res => {
          this.courses = res.result.course
          this.total_page = res.result.total_page
          this.resultType = res.result.search_type

          if (!this.courses[0]) {
            this.alertMsg = 'No courses were found'
            this.alert = true
          }

          // 搜到结果后关闭搜索动画
          this.courseListSpin = false
        }).catch(error => {
          console.log(error)
          this.courseListSpin = false
        })
      }

      // 每次翻页之后关闭已经打开的折叠面板
      this.panel = undefined
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

  .expansion-content {
    word-wrap: break-word;
    /* word-break: break-all; */
    float: left;
    text-align: left;
  }
</style>
