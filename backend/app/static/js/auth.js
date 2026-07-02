let authMode = "login";

const authModal = document.getElementById("authModal");
const openAuthBtn = document.getElementById("openAuthBtn");
const closeAuthBtn = document.getElementById("closeAuthBtn");
const authTitle = document.getElementById("authTitle");
const authSubmitBtn = document.getElementById("authSubmitBtn");
const switchAuthBtn = document.getElementById("switchAuthBtn");
const authSwitchText = document.getElementById("authSwitchText");
const authError = document.getElementById("authError");

const usernameInput = document.getElementById("usernameInput");
const emailInput = document.getElementById("emailInput");
const passwordInput = document.getElementById("passwordInput");

const userInfo = document.getElementById("userInfo");
const logoutBtn = document.getElementById("logoutBtn");

function openAuthModal() {
    authModal.classList.remove("hidden");
    authModal.classList.add("flex");
}

function closeAuthModal() {
    authModal.classList.add("hidden");
    authModal.classList.remove("flex");
    clearAuthError();
}

function showAuthError(message) {
    authError.textContent = message;
    authError.classList.remove("hidden");
}

function clearAuthError() {
    authError.textContent = "";
    authError.classList.add("hidden");
}

function setAuthMode(mode) {
    authMode = mode;
    clearAuthError();

    if (mode === "login") {
        authTitle.textContent = "Login";
        authSubmitBtn.textContent = "Login";
        usernameInput.classList.add("hidden");
        authSwitchText.textContent = "Don't have an account?";
        switchAuthBtn.textContent = "Register";
    } else {
        authTitle.textContent = "Register";
        authSubmitBtn.textContent = "Register";
        usernameInput.classList.remove("hidden");
        authSwitchText.textContent = "Already have an account?";
        switchAuthBtn.textContent = "Login";
    }
}

function saveUser(user) {
    localStorage.setItem("sitemind_user", JSON.stringify(user));
}

function getUser() {
    const user = localStorage.getItem("sitemind_user");
    return user ? JSON.parse(user) : null;
}

function clearUser() {
    localStorage.removeItem("sitemind_user");
}

function updateAuthUI() {
    const user = getUser();

    if (user) {
        openAuthBtn.classList.add("hidden");
        logoutBtn.classList.remove("hidden");
        userInfo.textContent = user.username;
    } else {
        openAuthBtn.classList.remove("hidden");
        logoutBtn.classList.add("hidden");
        userInfo.textContent = "Not logged in";
    }
}

async function handleAuthSubmit() {
    clearAuthError();

    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const username = usernameInput.value.trim();

    try {
        let user;

        if (authMode === "login") {
            user = await apiRequest("/auth/login", "POST", {
                email,
                password
            });
        } else {
            user = await apiRequest("/auth/register", "POST", {
                username,
                email,
                password
            });
        }

        saveUser(user);
        updateAuthUI();
        closeAuthModal();

        await ensureActiveChat();

    } catch (error) {
        showAuthError(error.message);
    }
}

openAuthBtn.addEventListener("click", () => {
    setAuthMode("login");
    openAuthModal();
});

closeAuthBtn.addEventListener("click", closeAuthModal);

switchAuthBtn.addEventListener("click", () => {
    setAuthMode(authMode === "login" ? "register" : "login");
});

authSubmitBtn.addEventListener("click", handleAuthSubmit);

logoutBtn.addEventListener("click", () => {
    clearUser();
    localStorage.removeItem("sitemind_current_chat");
    currentChatId = null;
    chatList.innerHTML = "";
    clearMessages();
    showWelcomeArea();
    updateAuthUI();
});

updateAuthUI();