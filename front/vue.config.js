const config = {
    publicPath: '',
    outputDir: '../back/web/',
    assetsDir: 'assets',
    configureWebpack: {
      devtool: 'source-map'
    }
}
// if (process.env.NODE_ENV === 'production') {
//     config.productionSourceMap = false;
// }
module.exports = config;
