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
          disabled
          plain
          :depressed="true"
          class="nav-btn"
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
            </v-sheet>
          </v-col>

          <v-col
            sm="10"
          >
              <v-card color="basil">
                <v-card-title class="text-center justify-center py-6">
                  <h1 class="font-weight-bold display-3 basil--text">
                    Course Creation Form
                  </h1>
                </v-card-title>

                <v-tabs
                  v-model="tab"
                  background-color="transparent"
                  color="basil"
                  grow
                >
                  <v-tab
                    v-for="item in tabItems"
                    :key="item"
                  >
                    {{ item }}
                  </v-tab>
                </v-tabs>

                <v-tabs-items v-model="tab">
                  <v-tab-item
                    v-for="item in tabItems"
                    :key="item"
                  >
                    <v-card
                      color="basil"
                      flat
                    >
                      <v-card-text
                        v-if="item=='Basic information'"
                      >
                        <v-row>
                          <el-form :model="courseForm" :rules="courseRules" ref="courseForm" label-width="150px" class="demo-ruleForm" style="margin-top: 30px;">
                            <el-form-item label="Course name" prop="name">
                              <el-input v-model="courseForm.name"></el-input>
                            </el-form-item>

                            <el-col :span="8">
                              <el-form-item label="Course code" prop="code">
                                <el-input v-model="courseForm.code"></el-input>
                              </el-form-item>
                            </el-col>
                            <el-col :span="8">
                              <el-form-item label="Course type" prop="type">
                                <el-input v-model="courseForm.type"></el-input>
                              </el-form-item>
                            </el-col>
                            <el-col :span="8">
                              <el-form-item label="Course unit" prop="unit">
                                <el-input-number v-model="courseForm.unit" :step="0.5"></el-input-number>
                              </el-form-item>
                            </el-col>
                            <el-col :span="8">
                              <el-form-item label="Department" prop="program">
                                <el-input v-model="courseForm.program"></el-input>
                              </el-form-item>
                            </el-col>
                            <el-col :span="6">
                              <el-form-item label="Academic year" prop="year">
                                <el-date-picker
                                  v-model="courseForm.year"
                                  type="year"
                                  placeholder="choose year"
                                  value-format="yyyy">
                                </el-date-picker>
                              </el-form-item>
                            </el-col>
                          </el-form>
                        </v-row>

                      </v-card-text>

                      <v-card-text
                        v-if="item=='CILO'"
                      >

                        <v-row style="margin-top: 10px;" v-if="uploadCILOFlag">
                          <v-col cols="12" md="12">
                            <a-upload-dragger
                              name="file"
                              :multiple="false"
                              accept=".xlsx"
                              action="/api/cilo/import_cilo"
                              maxCount=1
                              @change="handleImportCILO"
                            >
                              <p class="ant-upload-drag-icon">
                                <a-icon type="upload" />
                              </p>
                              <p class="ant-upload-text">
                                Click or drag file to this area to upload CILO
                              </p>
                              <p class="ant-upload-hint">
                                Note: Only .xlsx type file is supported. And the import function is only supported when you create a course.
                              </p>
                            </a-upload-dragger>
                          </v-col>
                        </v-row>

                        <v-row style="margin-top: 5%;">
                          <!-- <v-col cols="12" md="1"></v-col> -->
                          <!-- <v-col cols="12" md="4"> -->
                          <v-tooltip top>
                            <template v-slot:activator="{ on, attrs }">

                              <v-btn
                                style="margin-left: 50px;"
                                color="green lighten-2"
                                dark
                                outlined
                                tile
                                v-bind="attrs"
                                v-on="on"
                                @click="addCILO"
                              >
                                <v-icon dark>
                                  mdi-pencil-plus-outline
                                </v-icon>
                                <span
                                  style="margin-top: 3px; margin-left: 5px;"
                                  class="lower-letter-btn">Add CILO
                                </span>
                              </v-btn>

                            </template>
                            <span>Click here to add CILO</span>
                          </v-tooltip>
                          <span style="margin-left: 10px; margin-top: 10px;">Click here to download </span>
                          <v-hover>
                            <a
                              style="margin-left: 10px; margin-top: 10px; color: green;"
                              @click="getCILOTemplate"
                            >CILO_template.xlsx
                            </a>
                          </v-hover>

                        </v-row>

                        <!-- CILO Header -->
                        <v-row style="margin-top: 20px;">
                          <v-col cols="12" md="3">
                            <span>CILO INDEX</span>
                          </v-col>
                          <v-col md="4">
                            <span>CILO Content</span>
                          </v-col>
                          <v-col md="5">
                            <span>CILO Opeartion</span>
                          </v-col>
                        </v-row>

                        <v-row v-for="(item, key) in CILOLength" :key="key">
                          <v-col cols="12" md="3" style="margin-top: 10px;">
                            <span style="margin: 0 auto;">{{ key + 1 }}</span>
                          </v-col>
                          <v-col md="4">
                            <v-textarea
                              label="Input CILO Content Here"
                              auto-grow
                              outlined
                              rows="1"
                              row-height="15"
                              dense
                              clearable
                              counter
                              v-model="CILO[key]"
                            ></v-textarea>
                          </v-col>

                          <v-col md="5">
                            <v-tooltip top>
                              <template v-slot:activator="{ on, attrs }">
                                <v-btn
                                  color="blue lighten-2"
                                  dark
                                  outlined
                                  tile
                                  v-bind="attrs"
                                  v-on="on"
                                  @click="openSearchCourseDialog(key)"
                                >
                                  <v-icon dark>
                                    mdi-pencil-plus-outline
                                  </v-icon>
                                  <span
                                    style="margin-top: 3px; margin-left: 5px;"
                                    class="lower-letter-btn">Add Prerequisite relation
                                  </span>
                                </v-btn>
                              </template>
                              <span>Click here to add prerequisite CILO</span>
                            </v-tooltip>

                            <v-btn
                              style="margin-left: 10px;"
                              color="red lighten-2"
                              dark
                              outlined
                              tile
                              @click="deleteCILO(key)"
                            >
                              <v-icon dark>
                                mdi-delete
                              </v-icon>
                              delete
                            </v-btn>

                          </v-col>
                        </v-row>

                        <!-- 当prerequsite relation 有的时候才显示 -->
                        <v-divider v-if="prerequisiteCILORelation.length"></v-divider>

                        <v-row v-if="prerequisiteCILORelation.length">
                          <!-- <div style="height:calc(100vh - 50px);">
                            <RelationGraph
                              ref="seeksRelationGraph"
                              :options="graphOptions"
                              :on-node-click="onNodeClick"
                              :on-line-click="onLineClick"
                            />
                          </div> -->
                          <v-col cols="12" md="3">
                            <span>Current CILO INDEX</span>
                          </v-col>
                          <v-col md="4">
                            <span>Pre Course CILO Index</span>
                          </v-col>
                          <v-col md="5">
                            <span>Opeartion</span>
                          </v-col>
                        </v-row>

                        <v-row
                          v-for="(item, key) in prerequisiteCILORelation"
                          :key="item.currentCILOIndex + key"
                        >
                          <v-col cols="12" md="3" style="margin-top: 10px;">
                            <span>{{ item.currentCILOIndex }}</span>
                          </v-col>

                          <v-col md="4">
                            <v-chip
                              v-for="(item, inkey) in prerequisiteCILORelation[key]"
                              :key="item.chip + item.CILOIndex"
                              class="ma-2"
                              close
                              @click:close="removePrerequisiteCILO(key, inkey)"
                            >
                              {{ item.chip }}
                            </v-chip>
                          </v-col>

                          <v-col md="5">
                            <v-btn
                              color="red lighten-2"
                              dark
                              outlined
                              tile
                              @click="deleteCILOPrerequisite(key)"
                            >
                              <v-icon dark>
                                mdi-delete
                              </v-icon>
                              delete Pre
                            </v-btn>
                          </v-col>
                        </v-row>

                      </v-card-text>

                      <v-card-text
                        v-if="item=='Assessment'"
                      >
                        <v-row style="margin-top: 10px;" v-if="uploadAssessmentFlag">
                          <v-col cols="12" md="12">
                            <a-upload-dragger
                              name="file"
                              :multiple="false"
                              accept=".xlsx"
                              action="/api/assessment/import_assessment"
                              maxCount=1
                              @change="handleImportAssessment"
                            >
                              <p class="ant-upload-drag-icon">
                                <a-icon type="upload" />
                              </p>
                              <p class="ant-upload-text">
                                Click or drag file to this area to upload Assessment
                              </p>
                              <p class="ant-upload-hint">
                                Note: Only .xlsx type file is supported. And the import function is only supported when you create a course.
                              </p>
                            </a-upload-dragger>
                          </v-col>
                        </v-row>

                        <v-row style="margin-top: 5%;">
                          <v-tooltip top>
                            <template v-slot:activator="{ on, attrs }">

                              <v-btn
                                style="margin-left: 50px;"
                                color="green lighten-2"
                                dark
                                outlined
                                tile
                                v-bind="attrs"
                                v-on="on"
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

                            </template>
                            <span>Click here to add Assessment</span>
                          </v-tooltip>
                          <span style="margin-left: 10px; margin-top: 10px;">Click here to download </span>
                          <v-hover>
                            <a
                              style="margin-left: 10px; margin-top: 10px; color: green;"
                              @click="getAssessmentTemplate"
                            >Assessment_template.xlsx
                            </a>
                          </v-hover>

                        </v-row>

                        <!-- Assessment Header -->
                        <v-row style="margin-top: 20px;">
                          <v-col cols="12" md="3">
                            <span>Assessment Method</span>
                          </v-col>
                          <v-col md="3">
                            <span>Weight</span>
                          </v-col>
                          <v-col md="3">
                            <span>Corresponding CILOs</span>
                          </v-col>
                          <v-col md="3">
                            <span>Opeartion</span>
                          </v-col>
                        </v-row>

                        <v-row v-for="(ass, key) in assessment" :key="key">
                          <v-col cols="12" md="3">
                            <v-textarea
                              style="margin-left: 15px;"
                              label="method"
                              auto-grow
                              outlined
                              rows="1"
                              row-height="15"
                              dense
                              :clearable="true"
                              counter
                              v-model="ass.method"
                            ></v-textarea>
                          </v-col>
                          <v-col md="3">
                            <v-textarea
                              label="weight"
                              auto-grow
                              outlined
                              rows="1"
                              row-height="15"
                              dense
                              clearable
                              counter
                              v-model="ass.weight"
                            ></v-textarea>
                          </v-col>
                          <v-col md="3">
                            <v-textarea
                              label="CILOs"
                              auto-grow
                              outlined
                              rows="1"
                              row-height="15"
                              dense
                              clearable
                              counter
                              v-model="ass.CILOs"
                            ></v-textarea>
                          </v-col>
                          <v-col md="3">
                            <v-btn
                              color="red lighten-2"
                              dark
                              outlined
                              tile
                              @click="deleteAssessment(key)"
                            >
                              <v-icon dark>
                                mdi-delete
                              </v-icon>
                              delete
                            </v-btn>
                          </v-col>
                        </v-row>

                      </v-card-text>

                      <v-divider></v-divider>

                      <v-card-actions>
                        <v-container>
                          <v-btn
                            v-if="item!=='Basic information'"
                            color="deep-purple lighten-2"
                            dark
                            @click="gotoPreviousOperation"
                          >
                            <v-icon dark>
                              mdi-skip-previous
                            </v-icon>
                            Previous
                          </v-btn>
                          <v-btn
                            v-if="item!=='Assessment'"
                            color="deep-blue lighten-2"
                            dark
                            @click="gotoNextOperation"
                            style="margin-left: 20px;"
                          >
                            Next
                            <v-icon dark>
                              mdi-skip-next
                            </v-icon>
                          </v-btn>
                          <v-btn
                            v-if="item==='Assessment'"
                            color="green lighten-2"
                            dark
                            tile
                            @click="submitCreation"
                            style="margin-left: 20px;"
                          >
                            Submit
                          </v-btn>
                        </v-container>
                      </v-card-actions>

                    </v-card>

                  </v-tab-item>
                </v-tabs-items>
              </v-card>
              <course-cilo-list
                ref="CourseCiloList"
                v-bind:parentPreCILO="prerequisiteCILORelation"
                v-bind:currentCILOIndex="currentCILOIndex"
                @getPrerequisiteCILO="getPrerequisiteCILO"
              ></course-cilo-list>
              <leave-edit-warning ref="LeaveEditWarning"></leave-edit-warning>
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
import { createCourse } from '@/api/course'
import { getCILOTemplate } from '@/api/cilo'
import { getAssessmentTemplate } from '@/api/assessment'
import fileDownload from 'js-file-download'
import CourseCiloList from './modules/CourseCiloList'
import LeaveEditWarning from './modules/LeaveEditWarning.vue'
// import RelationGraph from 'relation-graph'
export default {
  name: 'CourseCreation',
  components: {
    CourseCiloList,
    LeaveEditWarning
    // RelationGraph
  },
  data: () => ({
    tab: 0,
    tabItems: [
      'Basic information', 'CILO', 'Assessment'
    ],
    breadItems: [
      {
        text: 'Dashboard',
        disabled: false,
        href: '/'
      },
      {
        text: 'Course Creation',
        disabled: true
      }
    ],
    guide_items: [
      'User Guide for Student',
      'User Guide for Lecturers',
      'User Guide for Course designer'
    ],

    valid: false,
    // courseCode: '',
    // courseType: '',
    // courseUnit: '',
    // courseName: '',
    // academicYear: '',
    // yearItems: [
    //   new Date().getFullYear(),
    //   new Date().getFullYear() + 1,
    //   new Date().getFullYear() + 2,
    //   new Date().getFullYear() + 3
    // ],
    // courseProgram: '',

    courseForm: {
      name: '',
      code: '',
      type: '',
      unit: 3,
      program: '',
      year: ''
    },
    courseRules: {
      name: [
        { required: true, message: 'please input course name', trigger: 'blur' }
      ],
      code: [
        { required: true, message: 'please input course code', trigger: 'blur' }
      ],
      type: [
        { required: true, message: 'please input course type', trigger: 'blur' }
      ],
      unit: [
        { required: true, message: 'please input course unit', trigger: 'blur' },
        { min: 0.0001, type: 'number', message: 'Unit must be positive' }
      ],
      program: [
        { required: true, message: 'please input course program', trigger: 'blur' }
      ],
      year: [
        { required: true, message: 'Please choose academic year', trigger: 'change' }
      ]
    },

    // courseCodeRules: [
    //   v => !!v || 'Course code is required'
    // ],
    // courseTypeRules: [
    //   v => !!v || 'Course type is required'
    // ],
    // courseUnitRules: [
    //   v => !!v || 'Course unit is required'
    // ],
    // courseNameRules: [
    //   v => !!v || 'Course name is required'
    // ],
    // courseProgramRules: [
    //   v => !!v || 'Program is required'
    // ],
    // courseYearRules: [
    //   v => !!v || 'Year is required'
    // ],

    // used for CILO
    CILOLength: 1,
    CILO: [],
    uploadCILOFlag: true, // 上传组件的显示: 初始为true

    prerequisiteCILORelation: [],
    currentCILOIndex: -1, // 当前点击添加 prerequisite 的 current CILO index
    // graphOptions: {
    //   // 参考"Graph 图谱"中的参数进行设置
    //   allowSwitchLineShape: true,
    //   allowSwitchJunctionPoint: true,
    //   defaultJunctionPoint: 'border'
    // }

    // used for assessment
    assessmentLength: 1,
    assessment: [
      {}
    ],
    uploadAssessmentFlag: true // 上传Assessment组件显示, 初始为true

  }),
  computed: {
    ...mapState({
      me: state => state.me
    })
  },
  watch: {
    // prerequisiteCILORelation (val) {
    //   console.log('this.prerequisiteCILORelation', val)
    // }
  },
  methods: {
    logout: function () {
      // logout 时删除 token
      this.$store.commit('del_token')
      this.$router.push({ name: 'Login' })
    },
    gotoDashboard: function () {
      if (this.courseForm.name || this.courseForm.code || this.courseForm.type || this.courseForm.program || this.courseForm.year ||
      this.CILO.length >= 2 || this.assessment[0].method || this.assessment[0].weight || this.assessment[0].CILOs) {
        this.$refs.LeaveEditWarning.openDialog('Dashboard')
      } else {
        this.$router.push({ name: 'Dashboard' })
      }
    },
    gotoDependencyVisualization: function () {
      if (this.courseForm.name || this.courseForm.code || this.courseForm.type || this.courseForm.program || this.courseForm.year ||
      this.CILO.length >= 2 || this.assessment[0].method || this.assessment[0].weight || this.assessment[0].CILOs) {
        // 如果正在编辑, 弹出框给个warning
        this.$refs.LeaveEditWarning.openDialog('DependencyVisualization')
      } else {
        // 如果没有填写内容, 直接走
        this.$router.push({ name: 'DependencyVisualization' })
      }
    },
    gotoNextOperation: function () {
      this.tab += 1
    },
    gotoPreviousOperation () {
      this.tab -= 1
    },
    addCILO () {
      this.CILOLength += 1
      this.CILO.push('')
    },
    deleteCILO (index) {
      // index starts from 0
      this.CILO.splice(index, 1)
      this.CILOLength -= 1
    },
    handleImportCILO (info) {
      const { status } = info.file
      switch (status) {
        case 'done': {
          // Load CILO excel file
          const res = info.file.response
          this.CILO = res.result.cilo_content
          this.CILOLength = this.CILO.length
          this.uploadCILOFlag = false // 隐藏上传组件
          this.$Message.success(`${info.file.name} file upload success`)
          break
        }
        case 'removed': {
          this.$Message.success(`${info.file.name} file removed`)
        }
      }
    },
    getCILOTemplate () {
      getCILOTemplate().then(res => {
        fileDownload(res, 'CILO_template.xlsx')
      })
    },
    addAssessment () {
      this.assessmentLength += 1
      this.assessment.push({
        method: '',
        weight: '',
        CILOs: ''
      })
    },
    deleteAssessment (index) {
      // index starts from 0
      this.assessment.splice(index, 1)
      this.assessmentLength -= 1
    },
    getAssessmentTemplate () {
      getAssessmentTemplate().then(res => {
        fileDownload(res, 'Assessment_template.xlsx')
      })
    },
    openSearchCourseDialog (key) {
      // 记录要添加dependency的current CILO index
      this.currentCILOIndex = key + 1
      // 打开添加面板
      this.$refs.CourseCiloList.openSearchDialog()
    },
    removePrerequisiteCILO (key, inkey) {
      this.prerequisiteCILORelation[key].splice(inkey, 1)
      // 如果删了最后一个chip, 将这一行直接删掉
      if (!this.prerequisiteCILORelation[key].length) {
        this.prerequisiteCILORelation.splice(key, 1)
      }
    },
    deleteCILOPrerequisite (key) {
      this.prerequisiteCILORelation.splice(key, 1)
    },
    getPrerequisiteCILO (pre) {
      // 拿到子组件回传的 this.prerequisiteCILO 数组
      this.prerequisiteCILORelation.push(pre)
      // 在CILO relation中添加 current CILO index
      this.prerequisiteCILORelation[this.prerequisiteCILORelation.length - 1].currentCILOIndex = this.currentCILOIndex
    },
    handleImportAssessment (info) {
      const { status } = info.file
      switch (status) {
        case 'done': {
          // Load assessment excel file
          const res = info.file.response
          this.assessment = res.result.assessment_content
          this.assessmentLength = this.assessment.length
          this.uploadAssessmentFlag = false // 隐藏上传组件
          this.$Message.success(`${info.file.name} file upload success`)
          break
        }
        case 'removed': {
          this.$Message.success(`${info.file.name} file removed`)
        }
      }
    },
    // showSeeksGraph (query) {
    //   const graphJsonData = {
    //     rootId: 'a',
    //     nodes: [
    //       { id: 'a', text: 'A', borderColor: 'yellow' },
    //       { id: 'b', text: 'B', color: '#43a2f1', fontColor: 'yellow' },
    //       { id: 'c', text: 'C', nodeShape: 1, width: 80, height: 60 },
    //       { id: 'e', text: 'E', nodeShape: 0, width: 150, height: 150 }
    //     ],
    //     links: [
    //       { from: 'a', to: 'b', text: '关系1', color: '#43a2f1' },
    //       { from: 'a', to: 'c', text: '关系2' },
    //       { from: 'a', to: 'e', text: '关系3' },
    //       { from: 'b', to: 'e', color: '#67C23A' }
    //     ]
    //   }
    //   // 以上数据中的node和link可以参考"Node节点"和"Link关系"中的参数进行配置
    //   this.$refs.seeksRelationGraph.setJsonData(graphJsonData, (seeksRGGraph) => {
    //     // Called when the relation-graph is completed
    //   })
    // },
    // onNodeClick (nodeObject, $event) {
    //   console.log('onNodeClick: ', nodeObject)
    // },
    // onLineClick (lineObject, $event) {
    //   console.log('onLineClick', lineObject)
    // },
    submitCreation () {
      // 查看是否填了必填项
      if (!(this.courseForm.name && this.courseForm.code && this.courseForm.type && this.courseForm.unit && this.courseForm.program &&
        this.courseForm.year)) {
        this.$Message.error('Incomplete Basic information')
        return
      }
      if (this.CILOLength <= 0 || !this.CILO[0]) {
        this.$Message.error('No CILO input')
        return
      }
      if (this.assessment.length <= 0) {
        this.$Message.error('No assessment input')
        return
      }
      // 查看所填的项是否valid
      var totalWeight = 0
      var methodList = []

      for (var i = 0; i < this.assessment.length; i++) {
        // 1. validate assessment method
        if (!this.assessment[i].method) {
          this.$Message.error('Assessment method fields are imcomplete')
          return
        } else {
          // 查看assessment method中有没有重复的
          if (methodList.indexOf(this.assessment[i].method) >= 0) {
            this.$Message.error('Some assessment methods are duplicated')
            return
          } else {
            if (i !== this.assessment.length - 1) {
              methodList.push(this.assessment[i].method)
            }
          }
        }

        // 2. validate assessment weight
        if (!this.assessment[i].weight) {
          this.$Message.error({ content: 'weight fields are imcomplete', duration: 4 })
          return
        } else {
          // 如果填写了weight, 检查weight合理性
          // 使用正则查看weight是不是个数字
          var integer = /^\d+$/ // 正整数
          var realNumberNotStartFrom0 = /^[1-9]\d*[.]\d+$/ // 不是0开头的实数
          var realNumberStartFrom0 = /^0[.]\d+$/ // 0开头的实数
          if (integer.test(this.assessment[i].weight) || realNumberNotStartFrom0.test(this.assessment[i].weight) || realNumberStartFrom0.test(this.assessment[i].weight)) {
            // 是数字
            const weight = Number(this.assessment[i].weight)
            // 查看weight是不是0
            if (weight === 0) {
              this.$Message.error({ content: 'Weight cannot be 0', duration: 4 })
              return
            }
            totalWeight += weight
          } else {
            // 如果不是数字
            this.$Message.error('weight must be a positive number')
            return
          }
        }

        // 3. validate assessment cILOs
        if (!this.assessment[i].CILOs) {
          this.$Message.error('The correspoding CILOs in assessment creation definition are imcomplete')
          return
        } else {
          // 判断corresponding CILOs是不是合理
          // 3.1 判断是不是按照格式的
          var CILOFormat = /^\d(-\d)*$/
          if (!(CILOFormat.test(this.assessment[i].CILOs))) {
            this.$Message.error('The corresponding CILO must follow the format like "1-2-3"!')
            return
          }
          // 3.2 判断是不是用了前面还没有定义的CILO
          // console.log(this.assessment[i].CILOs)
          // const correspondingCILOList = this.assessment[i].CILOs.split('-') // 将CILOs转换为数组
          // const sortedCILOList = correspondingCILOList.sort()
          // for (var j = 0; j < correspondingCILOList.length; j++) {
          //   // 3.4 检测corresponding CILO是不是填写了存在的CILO
          //   if (sortedCILOList[j] > this.CILOLength || sortedCILOList[j] < 1) {
          //     this.$Message.error('Non-existed CILO used in corresponding CILO')
          //     return
          //   }
          //   // 3.5 检测一个method中的corresponding CILO有没有重复
          //   if (j !== 0 && sortedCILOList[j] === sortedCILOList[j - 1]) {
          //     this.$Message.error('Duplicated corresponding CILOs in one method are detected!')
          //     return
          //   }
          // }
        }
      }
      if (totalWeight !== Number(1.0)) {
        this.$Message.error('The total weights in assessment do not equal to 1')
        return
      }

      // 创建课程
      createCourse({
        staffid: this.me.id,
        courseName: this.courseForm.name,
        courseCode: this.courseForm.code,
        courseType: this.courseForm.type,
        courseUnit: this.courseForm.unit,
        courseProgram: this.courseForm.program,
        academicYear: this.courseForm.year,
        CILO: this.CILO,
        assessment: this.assessment,
        preRelation: this.prerequisiteCILORelation
      }).then(res => {
        if (res.code === 200) {
          this.$Message.success(this.courseForm.code + ' ' + this.courseForm.name + 'is created successfully')
          this.$router.push({ name: 'Dashboard' })
        }
      }).catch(error => {
        this.$Message.error({ content: error, duration: 5 })
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
  .basil {
  background-color: #FFFFFF !important;
  }
  .basil--text {
    color: #356859 !important;
  }
</style>
