const path = require('path')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')
const BundleTracker = require('webpack-bundle-tracker')

const outPutPath = path.resolve(__dirname, 'static/bundles/')

module.exports = {
    entry: './src/main.js',
    output: {
        path: outPutPath,
        filename: '[name]-[hash].js',
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['css-loader']
            },
            {
                test: /\.s(a|c)ss$/,
                use: [
                    'style-loader',
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                          implementation: require('sass'),
                          sassOptions: {
                            fiber: require('fibers'),
                              indentedSyntax: true // optional
                          },
                        }
                    }
                ]
            },
            {
                test: /\.(jpe?g|avg|png|ico|gif)$/,
                loader: 'url-loader',
                options: {
                    limit: 2084,
                    name: './images/[name].[ext]',
                }
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.js$/,
                exclude: '/node_modules/',
                loader: 'babel-loader'
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new VuetifyLoaderPlugin(),
        new BundleTracker({filename: './webpack-stats.json'})
    ],
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve(__dirname, 'src/'),
        },
    },
    devServer: {
        contentBase: outPutPath
    }
}