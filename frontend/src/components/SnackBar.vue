<template>
  <v-snackbar
    v-model="visible"
    :color="color"
    top
    dark
    text
  >
    <!-- <v-icon :class="icon"></v-icon> -->
    {{ this.$store.state.snackbar.msg }}

    <template v-slot:action="{ attrs }">
        <v-btn
          v-if="showClose"
          :color="closeBtnColor"
          text
          v-bind="attrs"
          @click="close"
        >
          Close
        </v-btn>
      </template>
  </v-snackbar>
</template>

<script>
export default {
  name: 'SnackBar',
  data () {
    return {}
  },
  computed: {
    visible () {
      return this.$store.state.snackbar.visible
    },
    showClose () {
      return this.$store.state.snackbar.showClose
    },
    color () {
      return this.$store.state.snackbar.color
    },
    closeBtnColor () {
      return this.$store.state.snackbar.closeBtnColor
    }
  },
  methods: {
    close () {
      this.$store.commit('CLOSE_SNACKBAR')
    }
  }
}
</script>

<style lang="scss">
  .v-snack {
    .v-snack__content {
      justify-content: flex-start;
      i {
        margin-right: 10px;
      }
    }
  }
</style>
