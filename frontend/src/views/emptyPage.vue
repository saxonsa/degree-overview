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
          <template v-slot:activator="{attrs, on}">
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
          </template>

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
      <v-container>
        <v-row>
          <v-col
            cols="12"
            sm="2"
          >
            <v-sheet
              class="grey lighten-3"
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
            </v-sheet>
          </v-col>

          <v-col
            cols="12"
            sm="2"
          >
            <v-sheet
              class="grey lighten-3"
              min-height="100"
            >
              <!--  -->
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
import { mapState } from 'vuex'
export default {
  name: 'EmptyPage',
  data: () => ({
    guide_items: [
      'User Guide for Teacher',
      'User Guide for Student',
      'User Guide for New Staffs'
    ]
  }),
  computed: {
    ...mapState({
      me: state => state.me
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
