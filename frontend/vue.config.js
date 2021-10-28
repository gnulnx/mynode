module.exports = {
    devServer: {
      proxy: {
        '^/api': {
        // Use localhost if running locally and backend if via docker
          target: 'http://localhost:5000/',
        //   target: 'http://backend:5000/',
          changeOrigin: true,
          secure: false,
          pathRewrite: {'^/api': ''},
        },
      }
    }
  }