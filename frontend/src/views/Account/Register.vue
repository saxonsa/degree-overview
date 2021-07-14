<template>
  <div id="register">
    <v-container
      class="fill-height justify-center"
    >
      <v-row class="mx-auto">
        <v-col
          cols="12"
          offset-md="2"
          md="8"
        >
          <v-slide-y-transition>
            <v-card
              md="3"
              light
            >
              <pages-heading class="text-center display-3">
                Join Daffodil now
              </pages-heading>

              <v-row>
                <v-col
                  cols="12"
                  md="6"
                >
                  <v-row no-gutters>
                    <v-col
                      v-for="(section, i) in sections"
                      :key="i"
                      cols="12"
                    >
                      <v-list-item three-line>
                        <v-list-item-icon class="mr-4 mt-5 mt-md-4">
                          <v-icon
                            :large="$vuetify.breakpoint.mdAndUp"
                            :color="section.iconColor"
                            v-text="section.icon"
                          />
                        </v-list-item-icon>

                        <v-list-item-content>
                          <v-list-item-title
                            class="font-weight-light mb-4 mt-3"
                            v-text="section.title"
                          />

                          <v-list-item-subtitle v-text="section.text" />
                        </v-list-item-content>
                      </v-list-item>
                    </v-col>
                  </v-row>
                </v-col>

                <v-col
                  cols="12"
                  md="6"
                >
                  <div class="text-center">

                    <v-text-field
                      color="secondary"
                      label="Nickname..."
                      prepend-icon="mdi-face"
                      v-model="nickname"
                      :rules="[v => !!v || 'Please input nick name']"
                    />

                    <v-text-field
                      color="secondary"
                      label="Username..."
                      prepend-icon="mdi-account"
                      v-model="username"
                      :rules="[v => !!v || 'Please input your user name']"
                    />

                    <v-text-field
                      color="secondary"
                      label="Password..."
                      prepend-icon="mdi-lock-outline"
                      type="password"
                      v-model="password"
                      :rules="[v => !!v || 'Please input your password']"
                    />

                    <v-text-field
                      class="mb-8"
                      color="secondary"
                      label="Confirm Password..."
                      prepend-icon="mdi-lock"
                      type="password"
                      v-model="confirmPassword"
                      :rules="[v => !!v || 'Please input your password again']"
                    />

                    <v-checkbox
                      :input-value="checkAgreement"
                      color="secondary"
                    >
                      <template v-slot:label>
                        <span class="text-no-wrap" style="margin-top: 5px;" v-html="agreeText"></span>
                        <a
                          class="secondary--text ml-6 ml-sm-0 text-no-wrap"
                          href="#"
                          style="margin-top: 5px;"
                        >
                          terms and conditions
                        </a>.
                      </template>
                    </v-checkbox>

                    <pages-btn color="#81C784" @click="register">
                      Get Started
                    </pages-btn>

                    <div class="text-center grey--text body-1 font-weight-light" style="margin-top: 5%;">
                      Already have an account? Go to
                      <a href="/login">Login</a>
                    </div>

                  </div>
                </v-col>
              </v-row>
            </v-card>
          </v-slide-y-transition>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { userRegister } from '@/api/user.js'
export default {
  name: 'PagesRegister',

  components: {
    PagesBtn: () => import('./components/Btn'),
    PagesHeading: () => import('./components/Heading')
  },

  data: () => ({
    agreeText: 'I agree the &nbsp;',
    sections: [
      {
        icon: 'mdi-chart-timeline-variant',
        iconColor: 'primary',
        title: 'Marketing',
        text: 'We\'ve created the marketing campaign of the website. It was a very interesting collaboration.'
      },
      {
        icon: 'mdi-code-tags',
        iconColor: 'secondary',
        title: 'Fully Coded in HTML5',
        text: 'We\'ve developed the website with HTML5 and CSS3. The client has access to the code using GitHub.'
      },
      {
        icon: 'mdi-account-multiple',
        iconColor: 'cyan',
        title: 'Built Audience',
        text: 'There is also a Fully Customizable CMS Admin Dashboard for this product.'
      },
      {
        icon: 'mdi-account',
        iconColor: 'cyan',
        title: 'Built Audience',
        text: 'There is also a Fully Customizable CMS Admin Dashboard for this product.'
      }
    ],
    nickname: '',
    username: '',
    password: '',
    confirmPassword: '',
    checkAgreement: false
  }),
  methods: {
    register () {
      if (!this.nickname) {
        this.$store.dispatch('openSnackBar', {
          msg: 'Please input the nickname !!!'
        })
      } else if (!this.username) {
        this.$store.dispatch('openSnackBar', {
          msg: 'Please input the username !!!'
        })
      } else if (!this.password) {
        this.$store.dispatch('openSnackBar', {
          msg: 'Please input the password !!!'
        })
      } else if (!this.confirmPassword) {
        this.$store.dispatch('openSnackBar', {
          msg: 'Please confirm the password again in the confirm password field !!!',
          timeout: 8000
        })
      } else if (!this.checkAgreement) {
        this.$store.dispatch('openSnackBar', {
          msg: 'Please check the agreement !!!'
        })
      } else if (this.password !== this.confirmPassword) {
        this.$store.dispatch('openSnackBar', {
          msg: 'The confirm password does not match with the password !!!'
        })
      } else {
        userRegister({
          nickname: this.nickname,
          username: this.username,
          password: this.password
        }).then(res => {
          if (res.code === '200' && res.result === 1) {
            this.$router.push({ name: 'Login' })
            this.$store.dispatch('openSnackBar', {
              msg: 'Register success',
              color: 'black',
              closeBtnColor: '#4CAF50'
            })
          }
        }).catch(error => {
          console.error(error)
        })
      }
    }
  }
}
</script>

<style scoped>
  #register {
    background: url("../../assets/register.jpg") no-repeat;
    background-position: center;
    height: 100%;
    width: 100%;
    background-size: cover;
    position: fixed;
  }
</style>
