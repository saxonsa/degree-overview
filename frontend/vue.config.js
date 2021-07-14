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
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
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
