const path = require('path');
const webpack = require('webpack');


config = {
  entry: [
    './src/index.jsx'
  ],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        loaders: ['react-hot-loader/webpack', 'babel-loader'],
        exclude: /node_modules/,
        include: path.join(__dirname, 'src')
      },
      {
        test: /\.css$/i,
        include: path.join(__dirname, './src/components/Global.css'),
        use: [
          'style-loader',
          {
            loader: 'css-loader'
          },
        ],
      },
      {
        test: /\.css$/i,
        exclude: [
          /node_modules/,
          path.join(__dirname, './src/components/Global.css')
        ],
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              modules: true,
            },
          },
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg|eot|ttf|woff|woff2)$/i,
        exclude: /node_modules/,
        loader: 'url-loader',
        options: {
          limit: 8192,
        },
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.jsx']
  },
  output: {
    path: __dirname + '/../server/src/static/_scripts',
    publicPath: '/_scripts/',
    filename: 'bundle.js'
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development')
      }
    }),
    new webpack.IgnorePlugin(
        /(^fs$|cptable|jszip|xlsx|^es6-promise$|^net$|^tls$|^forever-agent$|^tough-cookie$|cpexcel|^path$|^react-native-fs$|^react-native-fetch-blob$)/
    )
  ]
};

// for local dev
if (JSON.stringify(process.env.NODE_ENV || 'development') == '"development"') {
  config.entry.push('webpack-dev-server/client?http://localhost:5007');
  config.entry.push('webpack/hot/only-dev-server');
  config.devServer = {
    contentBase: __dirname + '/../server/src/static',
    proxy: {
      '/': {
        target: 'http://127.0.0.1:9095',
        changeOrigin: true
      },
      '/_/api': {
        target: 'http://127.0.0.1:9095',
        changeOrigin: true
      }
    },
    hot: true,
    historyApiFallback: true,
    disableHostCheck: true
  };
}

module.exports = config;
