const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

module.exports = {
  entry: {
    frontend: './vsf/frontend/src/index.js',
  },
  output: {
    path: path.resolve("vsf/frontend/static/frontend/"),
    publicPath: "static/frontend/",
    filename: '[name]-[hash].js',
  },
  plugins: [
    new CleanWebpackPlugin(),
    new BundleTracker({
      path: path.resolve("vsf/"),
      filename: './webpack-stats.json',
    }),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {presets: ["@babel/env", "@babel/preset-react"]}
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  devServer: { writeToDisk: true, port: 2999 }
}