import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: { agentUpgrade: 'security' },
  /* config options here */
  reactCompiler: true,
};

export default nextConfig;
