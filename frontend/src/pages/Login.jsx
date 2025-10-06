import React from "react";
import { useAuth } from "@workos-inc/authkit-react";

export default function Login() {
  const { signIn } = useAuth();

  const handleLogin = async () => {
    // Kicks off hosted login; WorkOS will redirect back to /auth/callback
    await signIn();
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Login</h2>
      <p>Welcome to the WorkOS Full-Stack Application</p>
      <button
        onClick={handleLogin}
        style={{
          padding: "12px 24px",
          fontSize: "16px",
          backgroundColor: "#007bff",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Sign in with AuthKit
      </button>
    </div>
  );
}
