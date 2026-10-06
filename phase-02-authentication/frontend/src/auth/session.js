const SESSION_API_URL = "http://127.0.0.1:8000/api/accounts/session/";

export async function getSessionUser() {
  const response = await fetch(`${SESSION_API_URL}me/`, {
    method: "GET",
    credentials: "include",

    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    return null;
  }
  const data = await response.json();

  return data;
}


export async function loginSession(username, password) {
  const csrfToken = await getCsrfToken();

  if (csrfToken === null) {
    return {
      success: false,
      message: "Could not get CSRF token",
    };
  }

  const response = await fetch(`${SESSION_API_URL}login/`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      "X-CSRFToken": csrfToken,
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

  return {
    success: true,
    message: data.message,
  };
}


export async function logoutSession() {
  const csrfToken = await getCsrfToken();

  if (csrfToken === null) {
    return {
      success: false,
      message: "Could not get CSRF token",
    };
  }

  const response = await fetch(`${SESSION_API_URL}logout/`, {
    method: "POST",
    credentials: "include",
    headers: {
      Accept: "application/json",
      "X-CSRFToken": csrfToken,
    },
  });

  const data = await response.json();

  if (!response.ok) {
    return {
      success: false,
      message: data.detail || "Logout failed",
    };
  }

  return {
    success: true,
    message: data.message,
  };
}




export async function getCsrfToken() {
  const response = await fetch(`${SESSION_API_URL}csrf/`, {
    method: "GET",
    credentials: "include",
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    return null;
  }

  const data = await response.json();

  return data.csrfToken;
}