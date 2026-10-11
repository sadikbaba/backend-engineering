const JWT_API_URL = "http://127.0.0.1:8000/api/accounts/jwt/";

export async function loginJWT(username, password) {
  try {
    const response = await fetch(`${JWT_API_URL}login/`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });
    const data = await response.json();

    if (!response.ok) {
      return {
        success: false,
        message: data.error || data.detail || " Login Failed",
      };
    }

    sessionStorage.setItem("jwt_access", data.access);
    sessionStorage.setItem("jwt_refresh", data.refresh);
    return {
      success: true,
      message: "Login Successful",
    };
  } catch (error) {
    return {
      success: false,
      message: error.message,
    };
  }
}

export async function getJWTUser() {
  let access_token = sessionStorage.getItem("jwt_access");

  if (!access_token) {
    const refreshResult = await refreshJWT();

    if (!refreshResult.success) {
      return {
        success: false,
        message: refreshResult.message || "Not authenticated",
      };
    }

    access_token = refreshResult.access;
  }

  try {
    let response = await fetch(`${JWT_API_URL}me/`, {
      method: "GET",
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${access_token}`,
      },
    });

    // Access token failed → refresh once and retry once
    if (response.status === 401) {
      const refreshResult = await refreshJWT();

      if (!refreshResult.success) {
        return {
          success: false,
          message: refreshResult.message || "Not authenticated",
        };
      }

      access_token = refreshResult.access;

      response = await fetch(`${JWT_API_URL}me/`, {
        method: "GET",
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${access_token}`,
        },
      });
    }

    const data = await response.json();

    if (!response.ok) {
      return {
        success: false,
        message: data.detail || data.error || "Request failed",
      };
    }

    return {
      success: true,
      user: data,
    };
  } catch (error) {
    return {
      success: false,
      message: error.message,
    };
  }
}
export async function refreshJWT() {
  const refresh_token = sessionStorage.getItem("jwt_refresh");
  if (!refresh_token) {
    return {
      success: false,
      message: "Not authenticated",
    };
  }

  try {
    const response = await fetch(`${JWT_API_URL}refresh/`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh: refresh_token,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        success: false,
        message: data.detail || data.error || "Refresh failed",
      };
    }

    sessionStorage.setItem("jwt_access", data.access);

    return {
      success: true,
      access: data.access,
    };
  } catch (error) {
    return {
      success: false,
      message: error.message,
    };
  }
}

export async function logoutJWT() {
  const refresh_token = sessionStorage.getItem("jwt_refresh");

  if (!refresh_token) {
    return {
      success: false,
      message: "Not authenticated",
    };
  }

  try {
    const response = await fetch(`${JWT_API_URL}logout/`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        refresh: refresh_token,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        success: false,
        message: data.message || data.detail || data.error || "Logout failed",
      };
    }

    sessionStorage.removeItem("jwt_access");
    sessionStorage.removeItem("jwt_refresh");
    return {
      success: true,
      message: "Logout successful",
    };
  } catch (error) {
    return {
      success: false,
      message: error.message,
    };
  }
}

export async function registerJWT(username, password) {
  try {
    const response = await fetch(`${JWT_API_URL}register/`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        success: false,
        message: data.detail || data.error || "Register failed",
      };
    }

    return {
      success: true,
      message: data.message,
      username: data.username,
    };
  } catch (error) {
    return {
      success: false,
      message: error.message,
    };
  }
}
