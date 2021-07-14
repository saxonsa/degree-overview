<template>
  <div id="login">
    <v-container
      id="login-container"
      class="fill-height justify-center"
    >
      <v-overlay
        :z-index="0"
        :value="true"
        :opacity="0.2"
      >
        <v-card
          class="mx-auto"
          max-width="400"
          min-width="350"
        >
          <v-list-item two-line>
            <v-list-item-content>
              <div class="text-center">
                <v-icon class="vuetify-iconflower-daffodil"></v-icon>
                <hr/>
                <span class="login-title display-2 font-weight-bold mb-2">
                  DegreeOverview
                </span>
              </div>
            </v-list-item-content>
          </v-list-item>

          <v-card-text class="text-center">
            <v-row class="grid">
              <v-col sm="1">
                <v-icon class="vuetify-iconic_username" style="margin-top: 22px;"></v-icon>
              </v-col>
              <v-col>
                <v-text-field
                  v-model="username"
                  color="secondary"
                  :rules="usernameRules"
                  label="username..."
                  class="align-lg-end"
                  style="margin-left: 5px;"
                  type="text"
                />
              </v-col>
            </v-row>

            <v-row class="grid" style="margin-top: 0px;">
              <v-col sm="1">
                <v-icon class="vuetify-iconic_password" style="margin-top: 22px;"></v-icon>
              </v-col>
              <v-col>
                <v-text-field
                  v-model="password"
                  color="secondary"
                  label="password..."
                  :rules="passwordRules"
                  prepend-icon=""
                  type="password"
                  style="margin-left: 5px"
                />
              </v-col>
            </v-row>

            <v-row style="margin-top: 0px;">
                <v-radio-group row dense v-model="role">
                  <v-col>
                    <v-radio label="Student" value="student"></v-radio>
                  </v-col>
                  <v-col>
                    <v-radio label="Lecturer" value="lecturer"></v-radio>
                  </v-col>
                  <v-col>
                    <v-radio label="Designer" value="designer"></v-radio>
                  </v-col>
                </v-radio-group>
            </v-row>

            <v-btn
              normal
              depressed
              min-width="280"
              class="v-btn--text success--text"
              :loading="loginLoading"
              @click="login"
              @keyup.enter="login"
            >
              Login
            </v-btn>

            <div class="text-center grey--text body-1 font-weight-light" style="margin-top: 5%;">
              Lost password?
              <a href="/reset_password">Go to find password</a>
            </div>

          </v-card-text>
        </v-card>
      </v-overlay>
    </v-container>
  </div>
</template>

<script>
import { userLogin } from '@/api/user.js'
export default {
  data () {
    return {
      username: '',
      password: '',
      role: 'student',
      usernameRules: [
        v => !!v || 'Please input user name'
      ],
      passwordRules: [
        v => !!v || 'Please input your password'
      ],
      loginLoading: false
    }
  },
  created () {
    const that = this
    document.onkeydown = function (e) {
      e = window.event || e
      if (that.$route.path === '/login' && (e.code === 'Enter' || e.code === 'enter')) {
        that.login()
      }
    }
  },
  methods: {
    login: function () {
      if (!this.username) {
        this.$Message.error('No username input')
      } else if (!this.password) {
        this.$Message.error('No password input')
      } else {
        this.loginLoading = true
        userLogin({
          userId: this.username,
          password: this.password,
          role: this.role
        }).then(res => {
          switch (res.code) {
            case 200: {
              const token = res.result.token
              this.$store.commit('set_token', token)
              this.$store.commit('set_personal_info', res.result.me)
              this.$router.push({ name: 'Dashboard' })
              this.loginLoading = false
              break
            }
            case 3001: case 3002: case 3003: {
              this.loginLoading = false
              this.$Message.error(res.info)
              break
            }
          }
        }).catch(error => {
          console.log(error)
          this.loginLoading = false
        })
      }
    }
  }
}
</script>

<style scoped>
  #login {
    background: url("../../assets/login.jpg") no-repeat;
    background-position: center;
    height: 100%;
    width: 100%;
    background-size: cover;
    position: fixed;
  }
  .login-title {
    font-size: 30px;
  }
  .v-btn--text {
    margin-top: 10px;
  }
</style>
