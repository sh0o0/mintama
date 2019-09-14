const path = require('path')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')
const BundleTracker = require('webpack-bundle-tracker')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const UgligyJsPlugin = require('uglifyjs-webpack-plugin')
const OptimizeCssAssetsWebpackPlugin = require('optimize-css-assets-webpack-plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

const outPutPath = path.resolve(__dirname, 'static/bundles/')

module.exports = {
    entry: {
        main: './src/main.js',
        // test: './src/test.js',
    },
    output: {
        path: outPutPath,
        filename: '[name]-[hash].js',
    },
    module: {
        rules: [
            //eslintが使えない
            //原因：eslint-plugin-vue, vue-eslint-parserをインストールしているのに、インストールしろ言われる
            //とりあえずeslintはインストールはしたままにする
            //変更点：eslint関係インストール、.eslintrc.jsonの作成、webpack.config.jsへ追加
            // {
            //     enforce: 'pre',
            //     test: /\.jsx?/,
            //     exclude: /node_modules/,
            //     loader: 'eslint-loader'
            // },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                ]
            },
            {
                test: /\.s(c|a)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
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
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.jsx?$/,
                exclude: '/node_modules/',
                loader: 'babel-loader'
            },
            //url-loaderとfile-loaderの違いがわからない
            //現在の認識 
            //  url-loader:読み込み  
            //  file-loader:適用
            //どちらでも実装できるため、とりあえずすべてfile-loaderで実装
            //ただ、どちらも読み込んではくれない。また、いつか調べる。
            //material designなども読み込めないため、CSNにて実装
            {
                test: /\.(png|jpe?g|gif|svg|woff|woff2|ttf|eot|ico)$/,
                loader: 'file-loader',
                options: {
                    name: '[name]-[hash].[ext]',
                    outputPath: 'img/',
                    publicPath: path => '../img/' + path,
                },
            },
            //
            // {
            //     test: /\.(jpe?g|avg|png|ico|gif)$/,
            //     loader: 'url-loader',
            //     options: {
            //         limit: 2084,
            //         name: './images/[name].[ext]',
            //     }
            // },
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new VuetifyLoaderPlugin(),
        new BundleTracker({filename: './webpack-stats.json'}),
        new MiniCssExtractPlugin({filename: './css/index.css'}),
        // new CleanWebpackPlugin(),
    ],
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve(__dirname, 'src/'),
        },
        extensions: [".js", ".vue"]
    },
    optimization: {
        minimizer: [
            new UgligyJsPlugin({
                uglifyOptions: {
                    compress: {
                        drop_console: true,
                    }
                }
            }),
            new OptimizeCssAssetsWebpackPlugin({}),
        ]
    },
    devServer: {
        contentBase: outPutPath,
    },
    devtool: 'eval-source-map',
}