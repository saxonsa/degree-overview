<template>
  <div id="reset_password">
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
                Get your password back
              </pages-heading>

              <hr />

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
                      label="Username..."
                      prepend-icon="mdi-face"
                      v-model="username"
                      :rules="[v => !!v || 'Please input username']"
                      style="margin-top: 40px;"
                    />

                    <v-text-field
                      color="secondary"
                      label="Email to send instruction..."
                      prepend-icon="mdi-email"
                      v-model="email"
                      :rules="[v => !!v || 'Please input your email']"
                    />

                    <pages-btn color="#81C784" @click="findPassword" style="margin-top: 25px;">
                      Find Password
                    </pages-btn>

                    <div class="text-center grey--text body-1 font-weight-light" style="margin-top: 5%;">
                      Remember your password? Go to
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
import { userResetPassword } from '@/api/user.js'
export default {
  name: 'ResetPassword',
  components: {
    PagesBtn: () => import('./components/Btn'),
    PagesHeading: () => import('./components/Heading')
  },
  data () {
    return {
      sections: [
        {
          icon: 'mdi-chart-timeline-variant',
          iconColor: 'primary',
          title: 'User manual',
          text: '1. Please confirm the username is yourself, or there maybe some troubles happen.'
        },
        {
          icon: 'mdi-code-tags',
          iconColor: 'secondary',
          text: '2. After you click the \'Find password\' button, you will receive an email on your input email.'
        },
        {
          icon: 'mdi-account-multiple',
          iconColor: 'cyan',
          text: '3. Please follow the instruction to get your password back.'
        }
      ],
      username: '',
      email: ''
    }
  },
  methods: {
    findPassword () {
      console.log('username', this.username)
      console.log('email', this.email)
      if (this.username && this.email) {
        userResetPassword({
          username: this.username,
          email: this.email
        }).then(res => {
          console.log(res)
          this.$store.dispatch('openSnackBar', {
            msg: 'Reset function will be provided by ITSC, not our DegreeOverview system !!!',
            color: '#FFD54F',
            closeBtnColor: '#FFCC80'
          })
        })
      }
    }
  }
}
</script>

<style scoped>
#reset_password {
  background: url("../../assets/register.jpg") no-repeat;
  background-position: center;
  height: 100%;
  width: 100%;
  background-size: cover;
  position: fixed;
}
</style>
