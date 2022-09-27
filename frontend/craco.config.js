const path = require('path');

module.exports = {
    webpack: {
        eslint: { 
            enable: false
        },
        module: {
            rules: [
                {
                    test: /\.js$/,
                    enforce: "pre",
                    use: ["source-map-loader"]
                }
            ]
        },
        ignoreWarnings: [/Failed to parse source map/],
        alias: {
            '@components': path.resolve(__dirname, 'src/components/'),
            '@images': path.resolve(__dirname, 'src/images/')
        }
    }
}