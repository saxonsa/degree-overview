<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      persistent
      max-width="800px"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Define CILO Dependency</span>
        </v-card-title>

        <v-card-text>
          <v-row>
            <v-col cols="12" md="3">
              <v-select
                :items="selectOptions"
                label="Type"
                outlined
                dense
                v-model="selectOption"
              ></v-select>
            </v-col>
            <v-col md="9">
              <v-text-field
                solo
                v-model="searchKeyword"
                label="keyword..."
                clearable
                dense
              >
                <v-icon class="vuetify-iconsearch" role="button" slot="append" large color="blue lighten-1" @click="searchCourse"></v-icon>
              </v-text-field>
            </v-col>
          </v-row>

          <v-row v-if="prerequisiteCILO.length">
            <span style="margin-top: 15px; font-weight: 500; color: #3949AB">OR Relation (One of them should be satisfied): </span>
          </v-row>
          <v-row>
            <v-chip
              v-for="(item, key) in prerequisiteCILO"
              :key="item.chip"
              class="ma-2"
              close
              @click:close="removePrerequisiteCILO(key)"
            >
              {{ item.chip }}
            </v-chip>
          </v-row>

          <v-row style="margin-top: 0px;">
            <v-col cols="12" md="6">
              <a-spin tip="Loading" :spinning="courseListSpin">
                <v-list dense style="max-height: 400px;" class="overflow-y-auto">
                  <v-subheader>Course List</v-subheader>
                  <v-list-item-group
                    v-model="selectedCourseIndex"
                    color="blue"
                  >
                    <v-list-item
                      v-for="(course, i) in courseList"
                      :key="i"
                      @click="clickCourseItem(course)"
                    >
                      <!-- <v-list-item-icon v-if="selectedCourseIndex == i">
                        <v-icon>mdi-check</v-icon>
                      </v-list-item-icon> -->
                      <v-list-item-content>
                        <v-list-item-title v-text="course.course_code + '  ' + course.course_name"></v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </a-spin>
            </v-col>

            <v-col md="6">
              <a-spin tip="Loading" :spinning="CILOListSpin">
                <v-list dense style="max-height: 400px;" class="overflow-y-auto">
                  <v-subheader>CILO List</v-subheader>
                  <v-list-item-group
                    v-model="selectedCILOIndex"
                    color="green"
                  >
                    <v-list-item
                      v-for="(cilo, i) in CILOList"
                      :key="i"
                      @click="addCILOOnChip(cilo)"
                    >
                      <!-- <v-list-item-icon v-if="selectedCILOIndex == i">
                        <v-icon>mdi-check</v-icon>
                      </v-list-item-icon> -->
                      <v-list-item-content>
                        <v-list-item-title v-text="cilo.cilo_index + '.  ' + cilo.cilo_content"></v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </a-spin>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="confirmPrerequisiteCILO"
          >
            confirm
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import { searchCourseAllInDependency, searchCourseByKeywordInDependency } from '@/api/system.js'
export default {
  name: 'CourseCiloList',
  props: {
    parentPreCILO: {
      type: Array,
      default: null
    },
    currentCILOIndex: {
      type: Number,
      default: undefined
    }
  },
  data: () => ({
    dialog: false,
    searchKeyword: '',
    selectOptions: [
      'Course',
      'CILO'
    ],
    selectOption: 'Course',
    selectedCourseIndex: undefined,
    selectedCILOIndex: undefined,
    courseListSpin: false,
    CILOListSpin: false,
    courseList: [],
    CILOList: [],

    prerequisiteCILO: [],
    selectedCourseCode: null,
    selectCILOIndex: null
  }),
  watch: {
    selectedCourseIndex (selectedIndex) {
      if (selectedIndex === undefined) {
        this.CILOListSpin = true
        this.CILOList = []
        this.CILOListSpin = false
      } else {
        this.CILOListSpin = true
        this.CILOList = this.courseList[selectedIndex].cilo
        this.selectedCILOIndex = undefined
        this.CILOListSpin = false
      }
    },
    prerequisiteCILO (val) {
      console.log('prerequisiteCILO', val)
    }
  },
  methods: {
    openSearchDialog () {
      this.dialog = true
      this.courseListSpin = true

      // 初始化列表选中内容和样式
      this.selectedCourseIndex = undefined
      this.selectedCILOIndex = undefined

      this.searchKeyword = ''
      this.selectedIndex = undefined
      searchCourseAllInDependency().then(res => {
        this.courseList = res.result.course
        this.courseListSpin = false
      })
    },
    searchCourse () {
      this.courseListSpin = true

      if (!this.searchKeyword) {
        searchCourseAllInDependency().then(res => {
          this.courseList = res.result.course
          this.courseListSpin = false
        })
        return
      }

      searchCourseByKeywordInDependency({
        searchType: this.selectOption,
        searchKeyword: this.searchKeyword
      }).then(res => {
        this.courseList = res.result.course
        this.courseListSpin = false
      })
    },
    removePrerequisiteCILO (key) {
      this.prerequisiteCILO.splice(key, 1)
    },
    clickCourseItem (course) {
      this.selectedCourseCode = course.course_code
    },
    addCILOOnChip (CILO) {
      this.selectCILOIndex = CILO.cilo_index
      const combinedCourseCILO = this.selectedCourseCode + ' CILO' + this.selectCILOIndex
      for (var i = 0; i < this.prerequisiteCILO.length; i++) {
        if (this.prerequisiteCILO[i].chip === combinedCourseCILO) {
          this.prerequisiteCILO.splice(i, 1)
          return
        }
      }
      this.prerequisiteCILO.push({
        courseCode: this.selectedCourseCode,
        CILOIndex: this.selectCILOIndex,
        currentCILOIndex: this.currentCILOIndex,
        chip: this.selectedCourseCode + ' CILO' + this.selectCILOIndex
      })
      // const isInCILO = this.prerequisiteCILO.indexOf(combinedCourseCILO)
      // if (isInCILO >= 0) {
      //   this.prerequisiteCILO.splice(isInCILO, 1)
      // } else {
      //   this.prerequisiteCILO.push({
      //     courseCode: this.selectedCourseCode,
      //     CILOIndex: this.selectCILOIndex,
      //     currentCILOIndex: this.currentCILOIndex,
      //     chip: this.selectedCourseCode + ' CILO' + this.selectCILOIndex
      //   })
      // // this.prerequisiteCILO[this.prerequisiteCILO.length].courseCode = ''
      // // this.prerequisiteCILO[this.prerequisiteCILO.length - 1].courseCode = this.selectedCourseCode
      // }
    },
    confirmPrerequisiteCILO () {
      if (!this.prerequisiteCILO.length) {
        this.$Message.error('No CILO selected!')
      } else {
        // 看看是否有重复的prerequisite CILO relation被定义
        let duplicationFlag = false

        for (var i = 0; i < this.parentPreCILO.length; i++) {
          for (var j = 0; j < this.prerequisiteCILO.length; j++) {
            if (this.parentPreCILO[i].currentCILOIndex === this.currentCILOIndex) {
              for (var ii = 0; ii < this.parentPreCILO[i].length; ii++) {
                if (this.prerequisiteCILO[j].chip === this.parentPreCILO[i][ii].chip) {
                  this.$Message.error('Duplicated Relation detected!')
                  duplicationFlag = true
                  return
                }
              }
            }
          }
        }

        if (!duplicationFlag) {
          // 将 this.prerequisiteCILO 数组回传给父组件
          this.$emit('getPrerequisiteCILO', this.prerequisiteCILO)

          // 用于解决bug: 当添加完一个CILO的prerequisite后, 再添加下一个的时候会联动上一个的父组件中的内容进行修改,
          // 思路: 在传给父组件数组后直接清空dialog中的选择情况
          this.prerequisiteCILO = []

          this.dialog = false
        }
        // this.$emit('newCILOFlag', this.newCILORelationFlag)
        // this.$emit('getPrerequisiteCILO', this.prerequisiteCILO)
        // this.dialog = false
      }
    }
  }
}
</script>

<style scoped>
  .headline {
    font-size: 20px !important;
  }
</style>
