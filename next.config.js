/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    API: "",
    WS: "ws://127.0.0.1:9000",
    URL: "",
  },
};

module.exports = nextConfig;
