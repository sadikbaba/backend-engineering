import { getSessionUser, loginSession, logoutSession } from "./auth/session.js";

const app = document.querySelector("#app");

app.innerHTML = `
  <main>
    <h1>Session Authentication</h1>

    <form id="login-form">
      <input
        id="username"
        type="text"
        placeholder="Username"
        required
      />

      <input
        id="password"
        type="password"
        placeholder="Password"
        required
      />

      <button type="submit">
        Login
      </button>
    </form>

    <button id="check-session-button">
      Check Session
    </button>


    <button id="logout-button">
  Logout
    </button>
    <p id="session-status">
      Session not checked yet.
    </p>
  </main>
`;
const logoutButton = document.querySelector("#logout-button");
const loginForm = document.querySelector("#login-form");
const usernameInput = document.querySelector("#username");
const passwordInput = document.querySelector("#password");

const checkSessionButton = document.querySelector("#check-session-button");

const sessionStatus = document.querySelector("#session-status");

async function showSessionStatus() {
  const session = await getSessionUser();

  if (session === null) {
    sessionStatus.textContent = "Could not check session.";
    return;
  }

  if (session.authenticated) {
    sessionStatus.textContent = `Logged in as ${session.username}`;
    return;
  }

  sessionStatus.textContent = "Not logged in.";
}

async function handleLogin(event) {
  event.preventDefault();

  const username = usernameInput.value;
  const password = passwordInput.value;

  const result = await loginSession(username, password);

  if (!result.success) {
    sessionStatus.textContent = result.message;
    return;
  }

  await showSessionStatus();
}

loginForm.addEventListener("submit", handleLogin);

checkSessionButton.addEventListener("click", showSessionStatus);

async function handleLogout() {
  const result = await logoutSession();

  if (!result.success) {
    sessionStatus.textContent = result.message;
    return;
  }

  await showSessionStatus();
}

logoutButton.addEventListener("click", handleLogout);
showSessionStatus();

// token authentication
import { loginToken, getTokenUser, logoutToken } from "./auth/token.js";
// token authentication

app.insertAdjacentHTML(
  "beforeend",
  `
  <main>
    <h1>Token Authentication</h1>

    <form id="token-login-form">
      <input
        id="token-username"
        type="text"
        placeholder="Username"
        required
      />

      <input
        id="token-password"
        type="password"
        placeholder="Password"
        required
      />

      <button type="submit">
        Login
      </button>
    </form>

    <button id="check-token-button">
      Check Token
    </button>

    <button id="token-logout-button">
      Logout
    </button>

    <p id="token-status">
      Token not checked yet.
    </p>
  </main>
`
);

const tokenLoginForm = document.querySelector("#token-login-form");
const tokenUsernameInput = document.querySelector("#token-username");
const tokenPasswordInput = document.querySelector("#token-password");
const checkTokenButton = document.querySelector("#check-token-button");
const tokenLogoutButton = document.querySelector("#token-logout-button");
const tokenStatus = document.querySelector("#token-status");

async function showTokenStatus() {
  const result = await getTokenUser();

  if (!result.success) {
    tokenStatus.textContent = result.message;
    return;
  }

  tokenStatus.textContent = `Logged in as ${result.user.username}`;
}

async function handleTokenLogin(event) {
  event.preventDefault();

  const username = tokenUsernameInput.value;
  const password = tokenPasswordInput.value;

  const result = await loginToken(username, password);

  if (!result.success) {
    tokenStatus.textContent = result.message;
    return;
  }

  await showTokenStatus();
}

async function handleTokenLogout() {
  const result = await logoutToken();

  if (!result.success) {
    tokenStatus.textContent = result.message;
    return;
  }

  await showTokenStatus();
}

tokenLoginForm.addEventListener("submit", handleTokenLogin);
checkTokenButton.addEventListener("click", showTokenStatus);
tokenLogoutButton.addEventListener("click", handleTokenLogout);

showTokenStatus();