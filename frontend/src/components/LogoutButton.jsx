import React from "react";

/**
 * LogoutButton Component
 * Handles secure logout with WorkOS AuthKit by calling Django logout endpoint
 * which clears the WorkOS session and redirects to WorkOS logout URL
 */
export default function LogoutButton({
  onLogout,
  style = {},
  children = "Logout",
}) {
  const [isLoggingOut, setIsLoggingOut] = React.useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);

    try {
      // Step 1: Clear local JWT tokens first
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");

      // Step 2: Call logout callback if provided
      if (onLogout) {
        onLogout();
      }

      // Step 3: Call Django logout endpoint with credentials to handle WorkOS logout
      // This will:
      // - Load the WorkOS sealed session from wos_session cookie
      // - Get WorkOS logout URL from session.get_logout_url()
      // - Clear the wos_session cookie
      // - Return the WorkOS logout URL in JSON response
      const response = await fetch(
        `${process.env.REACT_APP_API_BASE}/logout/`,
        {
          method: "GET",
          credentials: "include", // Important: include cookies for WorkOS session
          headers: {
            Accept: "application/json",
          },
        }
      );

      // Step 4: Handle the JSON response
      if (response.ok) {
        const data = await response.json();

        // Django returns { logout_url: "...", message: "..." }
        if (data.logout_url) {
          // Redirect to WorkOS logout URL (or fallback login URL)
          window.location.href = data.logout_url;
        } else {
          // Fallback if no logout_url in response
          window.location.href = "/login";
        }
      } else {
        // If logout endpoint failed, still redirect to login as fallback
        console.error("Logout endpoint failed, redirecting to login");
        window.location.href = "/login";
      }
    } catch (error) {
      console.error("Logout error:", error);

      // Even if logout fails, redirect to login as fallback
      window.location.href = "/login";
    } finally {
      setIsLoggingOut(false);
    }
  };

  const buttonStyle = {
    padding: "12px 24px",
    fontSize: "16px",
    backgroundColor: "#dc3545",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: isLoggingOut ? "not-allowed" : "pointer",
    opacity: isLoggingOut ? 0.6 : 1,
    transition: "opacity 0.2s ease",
    ...style,
  };

  return (
    <button onClick={handleLogout} disabled={isLoggingOut} style={buttonStyle}>
      {isLoggingOut ? "Logging out..." : children}
    </button>
  );
}
