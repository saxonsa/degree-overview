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
        <!-- 可删除, 这个界面只有student能进来 -->
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

        <!-- Dependency Visualization -->
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
            md="3"
          >
            <v-sheet
              class="grey lighten-3"
              min-height="268"
            >
              <!--  -->
            </v-sheet>
          </v-col>

          <v-col
            md="9"
          >
            <v-sheet
              class="white"
              min-height="85vh"
            >
              <v-container></v-container> <!-- 占位DOM, 之后要优化一下这里 -->

              <!-- 模型选择框 -->
              <v-row cols="12">
                <v-col md="2" style="margin-top: 8px; margin-left: 10px;">
                  <span style="font-size: 18px;">Choose Model:</span>
                </v-col>
                <v-col md="8">
                  <el-select v-model="ciloCalculationModel" multiple placeholder="Choose performance model" medium style="width: 700px;">
                    <el-option
                      v-for="model in modelPool"
                      :key="model.value"
                      :label="model.label"
                      :value="model.value"
                    >
                      <span style="float: left">{{ model.value }}</span>
                      <span style="margin-left: 40px; font-size: 16px;">{{ model.label }}</span>
                    </el-option>
                  </el-select>
                </v-col>
              </v-row>
              <!-- Performance图表位置 -->
              <v-row cols="12" style="margin-top: 50px;">
                <v-col md="12">
                  <v-container id="ciloChart" style="width: 90%; height: 500px;" ref="ciloChart"></v-container>
                </v-col>
              </v-row>
              <v-row cols="12" style="margin-top: 30px">
                <a-table :columns="columns" :data-source="ciloData" style="width: 90%; margin-left: 50px;">
                  <span slot="name" slot-scope="text">{{ text }}</span>
                </a-table>
              </v-row>
            </v-sheet>
          </v-col>

        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
import { mapState } from 'vuex'
import storage from '@/utils/storage.js'
import { getStudentCILOScore } from '@/api/grade.js'
import { getCourseCILO } from '@/api/cilo.js'

export default {
  name: 'StudentPerformance',
  data: () => ({

    // CILO信息
    columns: [],
    ciloData: [],

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
        text: 'Student Performance',
        disabled: true
      }
    ],
    course: {
      code: '',
      name: ''
    },
    CILO: [],
    ciloChart: null, // CILO图表
    ciloCalculationModel: ['model1'], // 选择的model
    modelPool: [ // 所有的model
      {
        value: 'model1',
        label: 'SUM(score_of_assessment * 1 / total_numbers_of_corresponding_CILO)'
      },
      {
        value: 'model2',
        label: 'SUM(score_of_assessment)'
      }
    ]

  }),
  computed: {
    ...mapState({
      me: state => state.me
    })
  },
  created () {
    // 初始化界面获取 course code 和 course name
    this.course.code = this.$route.params.courseCode
    this.course.name = this.$route.params.courseName

    if (this.$route.params.courseCode === undefined) {
      this.course.code = storage.get('courseCode')
    } else {
      // 第一次进入课程performance
      if (storage.get('courseCode') === undefined) {
        storage.set('courseCode', this.$route.params.courseCode, 1400)
      }
    }

    if (this.$route.params.courseName === undefined) {
      this.course.name = storage.get('courseName')
    } else {
      // 第一次进入课程performance
      if (storage.get('courseName') === undefined) {
        storage.set('courseName', this.$route.params.courseName, 1400)
      }
    }

    this.breadItems[1].text = 'Performance on ' + this.course.code + ' ' + this.course.name

    this.$nextTick(() => {
      // 初始化Echarts
      this.ciloChart = this.$Echarts.init(this.$refs.ciloChart)
      this.generatePerformanceChart()
    })

    getCourseCILO({
      courseCode: this.course.code
    }).then(res => {
      this.CILO = res.result
      for (var i = 0; i < res.result.length; i++) {
        this.ciloData.push({
          key: (i + 1).toString(),
          CILOIndex: res.result[i].index,
          CILOContent: res.result[i].content
        })
      }
    })
  },
  mounted () {
    // 自适应
    const _this = this
    window.onresize = function () {
      _this.ciloChart.resize()
    }
  },
  watch: {
    ciloCalculationModel (val) {
      this.generatePerformanceChart()
      this.ciloChart.clear() // 更换method后刷新图表
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
    gotoDependencyVisualization: function () {
      this.$router.push({ name: 'DependencyVisualization' })
    },
    generatePerformanceChart () {
      this.ciloChart.showLoading({
        text: 'Loading performance data on CILO...',
        effect: 'whirling'
      })
      // 获取学生performance数据
      getStudentCILOScore({
        stuid: this.me.id,
        courseCode: this.course.code
      }).then(res => {
        const CILOLength = res.result.cilo_score.length
        var CILOArr = []
        var GradeArr = []
        for (var i = 0; i < CILOLength; i++) {
          CILOArr.push('CILO' + (i + 1).toString())
          GradeArr.push(res.result.cilo_score[i].cilo_performance)
        }

        // 随机生成第二个modle的数据
        var GradeArr2 = new Array(CILOLength)
        for (i = 0; i < CILOLength; i++) {
          var Range = 100 - 80
          var Random = Math.random()
          var num = 80 + Math.round(Random * Range)
          GradeArr2[i] = num
        }

        // legend
        var legend = []

        this.columns = [
          {
            title: 'CILO Index',
            dataIndex: 'CILOIndex',
            key: 'CILOIndex',
            scopedSlots: { customRender: 'CILOIndex' }
          },
          {
            title: 'CILO Content',
            dataIndex: 'CILOContent',
            key: 'CILOContent',
            ellipsis: true
          }
        ]
        for (i = 0; i < this.ciloCalculationModel.length; i++) {
          legend.push('model' + (i + 1).toString())

          // // CILO表格添加model表头
          // this.columns.push({
          //   title: 'model' + (i + 1).toString() + ' performance',
          //   dataIndex: 'model' + (i + 1).toString(),
          //   key: 'model' + (i + 1).toString()
          // })
        }

        // 生成Series
        var series = []
        for (i = 0; i < this.ciloCalculationModel.length; i++) {
          var model = {
            name: 'model' + (i + 1).toString(),
            type: 'bar',
            data: [],
            markPoint: {
              data: [
                { type: 'max' },
                { type: 'min' }
              ]
            },
            markLine: {
              data: [
                { type: 'average', name: 'Average' }
              ]
            }
          }
          if (this.ciloCalculationModel[i] === 'model1') {
            model.data = GradeArr
          } else if (this.ciloCalculationModel[i] === 'model2') {
            model.data = GradeArr2
          }

          series.push(model)
        }

        // 配置数据
        const option = {
          title: {
            text: 'Performance on CILO',
            subtext: ''
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: legend
          },
          toolbox: {
            show: true,
            feature: {
              dataView: { show: true, readOnly: false },
              magicType: { show: true, type: ['line', 'bar'] },
              restore: { show: true },
              saveAsImage: { show: true }
            }
          },
          calculable: true,
          xAxis: [
            {
              type: 'category',
              data: CILOArr
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: series
        }
        this.ciloChart.setOption(option)
        this.ciloChart.hideLoading()
      }).catch(error => {
        console.error(error)
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

  td.column-content {
    text-align: left !important;
  }
</style>
