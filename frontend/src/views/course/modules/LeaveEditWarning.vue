<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      max-width="350"
    >
      <v-card>
        <v-card-title class="headline">
          Are you sure to leave?
        </v-card-title>

        <v-card-text>
          All your edited information will be lost.
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            color="green darken-1"
            text
            @click="leave"
          >
            Leave
          </v-btn>

          <v-btn
            color="green darken-1"
            text
            @click="stay"
          >
            Stay
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
export default {
  name: 'LeaveEditWarning',
  data () {
    return {
      dialog: false,
      newPageName: ''
    }
  },
  methods: {
    openDialog (newPageName) {
      this.newPageName = newPageName
      console.log(this.newPageName)
      this.dialog = true
    },
    closeDialog () {
      this.dialog = false
    },
    leave () {
      this.dialog = false
      this.$router.push({ name: this.newPageName })
    },
    stay () {
      this.dialog = false
    }
  }
}
</script>
<style scoped>

</style>
