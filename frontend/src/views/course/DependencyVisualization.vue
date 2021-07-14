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

        <!-- Dependency visualization-->
        <v-btn
          disabled
          tile
          plain
          :depressed="true"
          class="nav-btn"
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
        <v-row cols="12">
          <v-col md="2" style="margin-top: 8px; margin-left: 10px;">
            <span style="font-size: 18px;">Choose type:</span>
          </v-col>
          <v-col md="2">
            <el-select v-model="visualizeType" placeholder="Dependency type" medium >
              <el-option
                v-for="type in typePool"
                :key="type"
                :value="type"
              >
              </el-option>
            </el-select>
          </v-col>
          <v-col md="2">
            <span style="font-size: 18px;">Choose program:</span>
          </v-col>
          <v-col md="2">
            <el-select v-model="program" placeholder="Dependency type" medium >
              <el-option
                v-for="program_choose in programList"
                :key="program_choose"
                :value="program_choose"
              >
              </el-option>
            </el-select>
          </v-col>
        </v-row>
        <a-spin tip="Loading visualization graph" :spinning="graphSpin">
          <div style="height:calc(100vh - 50px);">

              <RelationGraph
                ref="seeksRelationGraph"
                :options="graphOptions"
                :on-node-click="onNodeClick"
                :on-line-click="onLineClick"
              />

          </div>
        </a-spin>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
import { mapState } from 'vuex'
import RelationGraph from 'relation-graph'
import { getCourseDependencyAll, getAllProgram } from '@/api/course.js'
// import { getCILOContentByIndex } from '@/api/cilo.js'
export default {
  name: 'DependencyVisualization',
  components: {
    RelationGraph
  },
  data: () => ({
    guide_items: [
      'User Guide for Teacher',
      'User Guide for Student',
      'User Guide for New Staffs'
    ],
    breadItems: [
      {
        text: 'Dashboard',
        disabled: false,
        href: '/'
      },
      {
        text: 'Visualize Dependency',
        disabled: true
      }
    ],
    graphOptions: {
      // 参考"Graph 图谱"中的参数进行设置
      allowSwitchLineShape: true,
      allowSwitchJunctionPoint: true,
      defaultJunctionPoint: 'border',
      layouts: [
        {
          label: '自动布局',
          layoutName: 'force',
          layoutClassName: 'seeks-layout-force',
          distance_coefficient: 2
        }
      ]
    },
    program: 'CST',
    visualizeType: 'CILO',
    typePool: ['CILO', 'Course'],
    programList: [],

    graphJsonData: {},
    graphSpin: false
  }),

  computed: {
    ...mapState({
      me: state => state.me
    })
  },
  created () {
    getAllProgram().then(res => {
      console.log(res)
      this.programList = res.result
    })
  },
  mounted () {
    if (!this.visualizeType || this.visualizeType === 'CILO') {
      this.showSeeksGraph()
    } else if (this.visualizeType === 'Course') {
      this.showCourseGraph()
    }
  },
  watch: {
    visualizeType (type) {
      if (type === 'Course') {
        this.showCourseGraph()
      } else if (type === 'CILO') {
        this.showSeeksGraph()
      }
    },
    program (program) {
      if (this.visualizeType === 'Course') {
        this.showCourseGraph()
      } else if (this.visualizeType === 'CILO') {
        this.showSeeksGraph()
      }
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
    gotoCreateCourse () {
      this.$router.push({ name: 'CourseCreation' })
    },
    gotoAllCourse: function () {
      this.$router.push({ name: 'AllCourseForStudent' })
    },
    showCourseGraph (query) {
      this.graphSpin = true
      getCourseDependencyAll({
        courseProgram: this.program
      }).then(res => {
        this.graphJsonData = {
          rootId: '',
          nodes: [],
          links: []
        }

        // 添加nodes
        for (var i = 0; i < res.result.course_info.length; i++) {
          if (i === 0) {
            this.graphJsonData.rootId = '0'
          }
          console.log('here')
          this.graphJsonData.nodes.push({
            id: res.result.course_info[i].code,
            text: res.result.course_info[i].code,
            nodeShape: 1
          })
        }

        // 创建一个空node, 并让所有的node连接这个node后隐藏点和线
        this.graphJsonData.nodes.push({
          id: '0',
          text: '0',
          nodeShape: 0,
          width: 1,
          height: 1
        })

        for (var m = 0; m < res.result.course_info.length; m++) {
          this.graphJsonData.links.push({
            from: res.result.course_info[m].code,
            to: '0',
            lineWidth: 4,
            color: '#42A5F5',
            isHide: true
          })
        }

        // 添加links
        for (i = 0; i < res.result.course_relation.length; i++) {
          var to = res.result.course_relation[i].current
          var from = ''
          for (var j = 0; j < res.result.course_relation[i].pre.length; j++) {
            if (res.result.course_relation[i].pre[j].length === 1) {
              // and关系
              from = res.result.course_relation[i].pre[j][0]
              this.graphJsonData.links.push({
                from: from,
                to: to,
                lineWidth: 4,
                color: '#42A5F5'
              })
            } else if (res.result.course_relation[i].pre[j].length > 1) {
              // or 关系
              // 初始化一个空节点
              var id = ''
              for (var k = 0; k < res.result.course_relation[i].pre[j].length; k++) {
                id += res.result.course_relation[i].pre[j][k]
              }
              this.graphJsonData.nodes.push({
                id: id,
                text: 'or',
                width: 3,
                height: 1,
                color: '#7986CB',
                borderWidth: -1
              })
              // 子节点都连接上空节点
              for (k = 0; k < res.result.course_relation[i].pre[j].length; k++) {
                this.graphJsonData.links.push({
                  from: res.result.course_relation[i].pre[j][k],
                  to: id,
                  lineWidth: 4,
                  color: '#42A5F5'
                })
              }
              // 空节点连接父节点
              this.graphJsonData.links.push({
                from: id,
                to: to,
                lineWidth: 4,
                color: '#42A5F5'
              })
            }
          }
        }

        this.$nextTick(() => {
          // 以上数据中的node和link可以参考"Node节点"和"Link关系"中的参数进行配置
          this.$refs.seeksRelationGraph.setJsonData(this.graphJsonData, (seeksRGGraph) => {
            // Called when the relation-graph is completed
          })
        })
        this.graphSpin = false
      })
    },
    showSeeksGraph (query) {
      this.graphSpin = true
      getCourseDependencyAll({
        courseProgram: this.program
      }).then(res => {
        console.log('code', res.code)
        console.log('info', res.info)
        console.log('result', res.result)

        this.graphJsonData = {
          rootId: '',
          nodes: [],
          links: []
        }

        // 添加nodes
        for (var i = 0; i < res.result.cilo.length; i++) {
          if (i === 0) {
            // this.graphJsonData.rootId = res.result.cilo[i].course + ' ' + res.result.cilo[i].cilo
            this.graphJsonData.rootId = '0'
          }
          console.log('here')
          this.graphJsonData.nodes.push({
            id: res.result.cilo[i].course + ' ' + res.result.cilo[i].cilo,
            text: res.result.cilo[i].course + ' ' + res.result.cilo[i].cilo,
            nodeShape: 1
          })
        }

        // 创建一个空node, 并让所有的node连接这个node后隐藏点和线
        this.graphJsonData.nodes.push({
          id: '0',
          text: '0',
          nodeShape: 0,
          width: 1,
          height: 1
        })

        for (var m = 0; m < res.result.cilo.length; m++) {
          this.graphJsonData.links.push({
            from: res.result.cilo[m].course + ' ' + res.result.cilo[m].cilo,
            to: '0',
            lineWidth: 4,
            color: '#42A5F5',
            isHide: true
          })
        }

        // 添加Links关系
        for (i = 0; i < res.result.cilo_relation.length; i++) {
          var to = res.result.cilo_relation[i].current_course + ' ' + res.result.cilo_relation[i].current_cilo

          if (res.result.cilo_relation[i].pre_course.length === 1) {
            var from = res.result.cilo_relation[i].pre_course[0] + ' ' + res.result.cilo_relation[i].pre_cilo[0]
            this.graphJsonData.links.push({
              from: from,
              to: to,
              lineWidth: 4,
              color: '#42A5F5'
            })
          } else if (res.result.cilo_relation[i].pre_course.length > 1) {
            // 初始化一个空节点
            var id = ''
            for (var k = 0; k < res.result.cilo_relation[i].pre_course.length; k++) {
              id += res.result.cilo_relation[i].pre_course[k]
            }
            this.graphJsonData.nodes.push({
              id: id,
              text: 'or',
              width: 3,
              height: 1,
              color: '#7986CB',
              borderWidth: -1
            })
            // 将子节点连接空节点
            for (var j = 0; j < res.result.cilo_relation[i].pre_course.length; j++) {
              this.graphJsonData.links.push({
                from: res.result.cilo_relation[i].pre_course[j] + ' ' + res.result.cilo_relation[i].pre_cilo[j],
                to: id,
                lineWidth: 4,
                color: '#42A5F5'
              })
            }
            // 将空节点连接到父节点
            this.graphJsonData.links.push({
              from: id,
              to: to,
              lineWidth: 4,
              color: '#42A5F5'
            })
          }
        }

        // 添加links关系
        // for (i = 0; i < res.result.cilo_relation.length; i++) {
        //   var to = ''
        //   getCILOContentByIndex({
        //     course_code: res.result.cilo_relation[i].current_course,
        //     cilo_index: res.result.cilo_relation[i].current_cilo
        //   }).then(res => {
        //     to = res.result
        //   })

        //   var from = ''
        //   for (var j = 0; j < res.result.cilo_relation[i].pre_cilo.length; j++) {
        //     getCILOContentByIndex({
        //       course_code: res.result.cilo_relation[i].pre_course[j],
        //       cilo_index: res.result.cilo_relation[i].pre_cilo[j]
        //     }).then(res => {
        //       from = res.result
        //       graphJsonData.links.push({
        //         from: from,
        //         to: to
        //       })
        //       console.log(to)
        //     })
        //   }
        // }

        console.log(this.graphJsonData)

        this.$nextTick(() => {
          // 以上数据中的node和link可以参考"Node节点"和"Link关系"中的参数进行配置
          this.$refs.seeksRelationGraph.setJsonData(this.graphJsonData, (seeksRGGraph) => {
            // Called when the relation-graph is completed
          })
        })
        this.graphSpin = false
      })
    },
    onNodeClick (nodeObject, $event) {
      console.log('here node')
      console.log('onNodeClick: ', nodeObject)
      // console.log('here', this.graphJsonData)
      // this.$nextTick(() => {
      //   var graphJsonData = this.graphJsonData
      //   // this.showSeeksGraph()

      //   const clickCourse = nodeObject.text
      //   for (var i = 0; i < graphJsonData.links.length; i++) {
      //     if (graphJsonData.links[i].to === clickCourse) {
      //       graphJsonData.links[i].color = '#EF5350'
      //     }
      //   }
      //   console.log(graphJsonData)
      //   graphJsonData.rootId = 'CS001'
      //   // 以上数据中的node和link可以参考"Node节点"和"Link关系"中的参数进行配置
      //   this.$refs.seeksRelationGraph.setJsonData(graphJsonData, (seeksRGGraph) => {
      //   // Called when the relation-graph is completed
      //   })
      // })
    },
    onLineClick (lineObject, $event) {
      console.log('onLineClick', lineObject)
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
