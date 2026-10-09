const API_URL = "http://127.0.0.1:8000/api/accounts/token/";

export async function loginToken(username, password) {
  try {
    const response = await fetch(`${API_URL}login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
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
        message: data.error || data.detail || "Login failed",
      };
    }

    sessionStorage.setItem("token", data.token);
    return {
      success: true,
      message: data.token,
    };
  } catch (error) {
    return {
      success: false,
      message: error.message,
    };
  }
}

// get token from sessionStorage

export async function getTokenUser() {
  const token = sessionStorage.getItem("token");
  if (!token) {
    return {
      success: false,
      message: "not authenticated",
    };
  }

  try {
    const response = await fetch(`${API_URL}me/`, {
      method: "GET",
      headers: {
        Accept: "application/json",
        Authorization: `Token ${token}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      sessionStorage.removeItem("token");
      return {
        success: false,
        message: data.error || data.detail || "not authenticated",
      };
    }

    return { success: true, user: data };
  } catch (error) {
    return {
      success: false,
      message: error.message,
    };
  }
}


// logout

export async function logoutToken() {
  const token = sessionStorage.getItem("token");
  if (!token) {
    return {
      success: false,
      message: "not authenticated",
    };
  }

  try {
    const response = await fetch(`${API_URL}logout/`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        Authorization: `Token ${token}`,
      },
    });

    const data = await response.json();
    if (!response.ok) {
      return {
        success: false,
        message: data.error || data.detail || "Logout failed",
      };
    }

    sessionStorage.removeItem("token");
    return {
      success: true,
      message: data.message,
    };
  } catch (error) {
    return {
      success: false,
      message: error.message,
    };
  }
}
