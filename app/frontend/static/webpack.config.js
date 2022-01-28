/*
 * Copyright (C) 2020 University of Konstanz -  Data Analysis and Visualization Group
 * This file is part of SciBib <https://github.com/dbvis-ukon/SciBib>.
 *
 * SciBib is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SciBib is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SciBib.  If not, see <http://www.gnu.org/licenses/>.
 */

const webpack = require('webpack');
const resolve = require('path').resolve;

var path = require('path');

const config = {
    devtool: "eval-source-map",
    entry: __dirname + '/js/index.js',
    output: {
        path: resolve('./'),
        filename: 'bundle.js',
        publicPath: '/static/'
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
                use: [
                    {loader: 'style-loader'},
                    {loader: 'css-loader'},
                    {loader: 'sass-loader'}]
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-env']
                }
            },
            {
                test: /.(ttf|otf|eot|svg|woff(2)?)(\?[a-z0-9]+)?$/,
                type: 'assset/resource',
                dependency: { not: ['url'] },
            }
        ]
    }
};

module.exports = config;

