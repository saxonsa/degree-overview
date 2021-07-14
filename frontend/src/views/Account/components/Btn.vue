<script>
import { VBtn } from 'vuetify/lib'

export default {
  name: 'PagesBtn',

  extends: VBtn,

  props: {
    color: {
      type: String,
      default: '  '
    },
    depressed: {
      type: Boolean,
      default: false
    },
    default: {
      type: Boolean,
      default: true
    },
    rounded: {
      type: Boolean,
      default: true
    }
  }
}
</script>
