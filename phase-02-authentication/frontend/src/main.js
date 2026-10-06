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