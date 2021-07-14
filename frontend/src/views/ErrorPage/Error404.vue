<template>
  <v-card
    style="margin-top: 8%;"
    class="mx-auto"
    width="1000"
    height="700"
  >
    <v-img
      src="../../assets/error.svg"
      height="500"
      width="800"
    ></v-img>

    <v-card-actions>
      <v-btn
        color="orange lighten-2"
        text
      >
        Why are you here? Give us more details for improvement...
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn
        icon
        @click="show = !show"
      >
        <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
      </v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="show">
        <v-divider></v-divider>

        <v-card-text>
          Hi! Here is 404 error page. Why are you here?
        </v-card-text>

        <v-btn rounded color="#1565C0" dark @click="gotoDashboard">Send me back</v-btn>
      </div>
    </v-expand-transition>
  </v-card>
</template>
<script>
export default {
  name: 'Error404',
  data () {
    return {
      show: true
    }
  },
  methods: {
    gotoDashboard () {
      this.$router.push({ name: 'Dashboard' })
    }
  }
}
</script>
