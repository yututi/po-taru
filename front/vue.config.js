const config = {
    publicPath: '',
    outputDir: '../back/web/',
    assetsDir: 'assets',
    filenameHashing: false
}
if (process.env.NODE_ENV === 'production') {
    config.productionSourceMap = false;
}
module.exports = config;