import React from "react";
import api from "../api";
import { useAuth } from "@workos-inc/authkit-react";

export default function Dashboard() {
  const [msg, setMsg] = React.useState("");
  const [loading, setLoading] = React.useState(true);
  const { user, getAccessToken, isLoading, signIn, signUp, signOut } =
    useAuth();

  React.useEffect(() => {
    api
      .get("/hello")
      .then((res) => {
        setMsg(res.data.message);
        setLoading(false);
      })
      .catch((e) => {
        setMsg(`Error: ${e.message}`);
        setLoading(false);
      });
    console.log("User info:", user);
  }, []);

  const handleLogout = () => {
    signOut();
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.assign("/login");
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Dashboard</h2>
      <div style={{ marginBottom: 20 }}>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <p
            style={{
              padding: "16px",
              backgroundColor: "#f8f9fa",
              border: "1px solid #dee2e6",
              borderRadius: "4px",
            }}
          >
            {msg}
          </p>
        )}
      </div>
      <button
        onClick={handleLogout}
        style={{
          padding: "12px 24px",
          fontSize: "16px",
          backgroundColor: "#dc3545",
          color: "white",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </div>
  );
}
