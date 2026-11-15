import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: { agentUpgrade: 'security' },

  reactCompiler: true,
};

export default nextConfig;
