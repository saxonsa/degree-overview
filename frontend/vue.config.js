module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  css: {
    loaderOptions: {
      less: {
        javascriptEnabled: true
      }
    }
  },
  devServer: {
    host: '0.0.0.0',
    port: 9001,
    proxy: {
      '/api': {
        target: 'http://8.134.64.20:5101',
        secure: false,
        // ws: false,
        changeOrigin: true,
        pathRewrite: { '^/api': '' }
      }
    },
    hot: true,
    open: true
  }
}
