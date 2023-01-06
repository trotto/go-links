/** @type {import('next').NextConfig} */
const nextConfig = {
  // reactStrictMode: true,
  // swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/:path*',
        destination: 'http://127.0.0.1:9095/:path*' // Proxy to Backend
      },
      {
        source: '/_/api/:path*',
        destination: 'http://127.0.0.1:9095/_/api/:path*' // Proxy to Backend
      }
    ]
  }
}

module.exports = nextConfig
