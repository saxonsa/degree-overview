import moment from 'moment'

var storage = {
  /* key 保存键
     *value 保存内容 localSorage 不能保存 Object 对象 需要使用 stringify 进行转换
     * expired 失效时间 定义 单位 分钟
     */
  set (key, value, expired) {
    /* 定义 source 临时 对象 临时存储 key value 赋值后 加入到 localStorage */
    const source = { key: key, value: value }

    /* now 获取当前时间 */
    const now = Date.now()
    /* 1 分钟计算 (1000*60)  计算出总失效时间 (1000 * 60 * expired) now + 失效总分钟 算出最大存储时间 */
    if (expired) {
      source.value = JSON.stringify({ data: value, expired: now + (1000 * 60 * expired) })
    } else {
      // 默认 localstorage保存1天时间 --> 1440分钟
      source.value = JSON.stringify({ data: value, expired: now + (1000 * 60 * 1440) })
    }
    localStorage.setItem(source.key, source.value)
  },
  get (key) {
    const now = Date.now()

    const source = { key: key, value: null }

    /* 获取 localStorage 存储信息 赋值给 source 对象 */
    // 修复bug: localStorage.getItem(key) 返回的是一个string类型, source.value.data获取不到值
    // 修复方法: 用JSON.parse 将String转换为Object
    // 修复人: Saxon SA
    // Fix time: 2021/5/12
    source.value = JSON.parse(localStorage.getItem(key))

    /* 如果key 有效  判断当前时间 是否超过 失效时间 */
    if (source.value) {
      if (source.value.expired) {
        if (now >= source.value.expired) {
          /* 超过失效时间 删除 储存内容  */
          this.remove(source.key)
        } else {
          return source.value.data
        }
      } else {
        return source.value.data
      }
    }
  },
  remove (key) {
    localStorage.removeItem(key)
  },
  expiredtime (key) {
    // 获取失效时间
    const now = Date.now()

    const source = { key: key, value: null }
    /* 从缓存中取出 信息 */
    source.value = JSON.parse(localStorage.getItem(source.key))

    /* 判断 key 是否失效 */
    if (source.value) {
      /* 获取失效时间 */
      const expired = source.value.expired
      source.value.expired = source.value.expired = moment(expired).diff(moment(now), 'seconds')
      return source.value.expired
    } else {
      // 已经失效
      return false
    }
  }
}

/* export default  用于导出 函数   类中只能定义一个 其他类通过此对象可调用 该类所有方法 */
export default storage
