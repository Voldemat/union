const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { SourceMapDevToolPlugin } = require('webpack');

module.exports = {
    entry: path.resolve(__dirname, 'src', 'index.js'),
    output:{
        path: path.resolve(__dirname, 'dist'),
        filename: '[contenthash].bandle.js',
        clean: true
    },
    module:{
        rules:[
            {
                test: /\.js$/,
                exclude:/node_modules/,
                use: [
                    {
                        loader:'babel-loader',
                        options:{
                            sourceMaps:true,
                            presets:[
                                '@babel/preset-env',
                                '@babel/preset-react'
                            ]
                        }
                    },
                ]
            },
            {
                test:/\.js$/,
                enforce: 'pre',
                use:['source-map-loader']
            },
            {
                test: /\.css$/,
                use:['style-loader', 'css-loader']
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/,
                use:['file-loader']
            }
        ]
    },
    plugins:[
        new HtmlWebpackPlugin({
            template: path.resolve(__dirname, 'src', 'index.html')
        }),
        new SourceMapDevToolPlugin({
            filename:"[file].map"
        })
    ],
    devServer:{
        contentBase: path.resolve(__dirname, 'dist'),
        compress: true,
        port: 9000,
        historyApiFallback: true,
        hot: true,
    }
}