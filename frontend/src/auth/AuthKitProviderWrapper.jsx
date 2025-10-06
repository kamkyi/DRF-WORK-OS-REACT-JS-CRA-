import React from "react";
import { AuthKitProvider, useAuth } from "@workos-inc/authkit-react";

export const AuthProviderRoot = ({ children }) => {
  return (
    <AuthKitProvider
      clientId={process.env.REACT_APP_WORKOS_CLIENT_ID}
      redirectUri={process.env.REACT_APP_WORKOS_REDIRECT_URI}
    >
      {children}
    </AuthKitProvider>
  );
};

// Helper hook (optional)
export { useAuth };
