/**
 * @param msg 信息
 * @param color snackbar 颜色
 * @param closeBtnColor snackbar 关闭按钮的颜色
 * @param visible 是否可见
 * @param showClose 关闭按钮
 * @param timeout 停留持续时间
 */

const snackbar = {
  namespace: true,
  state: {
    msg: '',
    color: '',
    closeBtnColor: '',
    visible: false,
    showClose: true,
    timeout: 5000
  },
  mutations: {
    OPEN_SNACKBAR (state, options) {
      state.visible = true
      state.msg = options.msg
      state.color = options.color
      state.closeBtnColor = options.closeBtnColor
      if (options.timeout) {
        state.timeout = options.timeout
      }
    },
    CLOSE_SNACKBAR (state) {
      state.visible = false
    },
    setShowClose (state, isShow) {
      state.showClose = isShow
    },
    setTimeout (state, timeout) {
      state.timeout = timeout
    }
  },
  actions: {
    openSnackBar (context, options) {
      const timeout = context.state.timeout
      context.commit('OPEN_SNACKBAR', {
        msg: options.msg,
        color: options.color,
        closeBtnColor: options.closeBtnColor ? options.closeBtnColor : '#E91E63'
      })
      setTimeout(() => {
        context.commit('CLOSE_SNACKBAR')
      }, timeout)
    }
  }
}

export default snackbar
