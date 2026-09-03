/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  // Decoupled API architecture: browser directly communicates with Render FastAPI
};

export default nextConfig;
