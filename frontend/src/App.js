import React from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  useNavigate,
  useSearchParams,
} from "react-router-dom";
import { AuthProviderRoot } from "./auth/AuthKitProviderWrapper";
import ProtectedRoute from "./auth/ProtectedRoute";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import api from "./api";

function AuthCallback() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = React.useState("Processing...");

  React.useEffect(() => {
    console.log("Auth params:", params.toString());
    const code = params.get("code");
    const idToken = params.get("id_token"); // optional fallback

    if (!code && !idToken) {
      setStatus("No authentication code received");
      setTimeout(
        () => navigate("/login?error=no_code", { replace: true }),
        2000
      );
      return;
    }

    const payload = code ? { code } : { id_token: idToken };

    api
      .post("/auth/workos/callback", payload)
      .then(({ data }) => {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        setStatus("Login successful! Redirecting...");
        setTimeout(() => navigate("/", { replace: true }), 1000);
      })
      .catch((e) => {
        console.error("Auth error:", e);
        setStatus("Authentication failed. Redirecting to login...");
        setTimeout(
          () => navigate("/login?error=auth_failed", { replace: true }),
          2000
        );
      });
  }, [params, navigate]);

  return (
    <div style={{ padding: 24, textAlign: "center" }}>
      <h2>Authentication</h2>
      <p>{status}</p>
    </div>
  );
}

export default function App() {
  return (
    <AuthProviderRoot>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/auth/callback" element={<AuthCallback />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProviderRoot>
  );
}
