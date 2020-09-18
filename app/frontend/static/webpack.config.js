const webpack = require('webpack');
const resolve = require('path').resolve;

var path = require('path');

const config = {
    devtool: "eval-source-map",
    entry: __dirname + '/js/index.js',
    output: {
        path: resolve('./'),
        filename: 'bundle.js',
        publicPath: resolve('./')
    },
    resolve: {
        alias: {
            js: path.resolve(__dirname, 'js')
        },
        extensions: ['.js', '.css']
    },
    module: {
        rules: [
            {
                test: /\.s?css$/,
                //loader: 'style-loader! css-loader?modules'
                loader: ['style-loader', 'css-loader', 'sass-loader']
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                query: {
                    presets: ['@babel/preset-env']
                }
            },
            {
                test: /.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
                use: [{
                    loader: 'file-loader',
                    options: {
                        name: '[name].[ext]',
                        outputPath: 'fonts/',    // where the fonts will go
                        publicPath: '/static/fonts/'       // override the default path
                    }
                }]
            }
        ]
    }/*,
    plugins: [
        new webpack.ProvidePlugin({
            '$': 'jquery',
            jQuery: 'jquery',
            'window.$': 'jquery',
            'window.jQuery': 'jquery'
            //'$.sortable' : ['jquery-sortablejs', 'Sortable']
        })
    ]/*,
    node: {
        fs: 'empty'
    }*/
};

module.exports = config;

