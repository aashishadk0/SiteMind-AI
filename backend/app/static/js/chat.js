let currentChatId = null;

let selectedProvider = "ollama";
let selectedModel = "llama3.2:latest";

const chatList = document.getElementById("chatList");
const messagesBox = document.getElementById("messages");
const welcomeScreen = document.getElementById("welcomeScreen");
const newChatBtn = document.getElementById("newChatBtn");

function showMessagesArea() {
    welcomeScreen.classList.add("hidden");
    messagesBox.classList.remove("hidden");
}

function showWelcomeArea() {
    welcomeScreen.classList.remove("hidden");
    messagesBox.classList.add("hidden");
}

function renderMessage(role, content) {
    showMessagesArea();

    const wrapper = document.createElement("div");

    if (role === "user") {
        wrapper.className = "flex justify-end mb-5";
        wrapper.innerHTML = `
            <div class="max-w-[75%] rounded-2xl rounded-br-md bg-green-600 px-5 py-3 text-white leading-relaxed">
                ${escapeHtml(content)}
            </div>
        `;
    } else {
        wrapper.className = "flex justify-start mb-5";
        wrapper.innerHTML = `
            <div class="max-w-[80%] rounded-2xl rounded-bl-md bg-[#2b2b2b] border border-[#3a3a3a] px-5 py-3 text-gray-100 leading-relaxed whitespace-pre-wrap">
                ${escapeHtml(content)}
            </div>
        `;
    }

    messagesBox.appendChild(wrapper);
    scrollToBottom();
}

function renderLoadingMessage() {
    showMessagesArea();

    const wrapper = document.createElement("div");
    wrapper.id = "loadingMessage";
    wrapper.className = "flex justify-start mb-5";
    wrapper.innerHTML = `
        <div class="max-w-[80%] rounded-2xl rounded-bl-md bg-[#2b2b2b] border border-[#3a3a3a] px-5 py-3 text-gray-300">
            Generating reply...
        </div>
    `;

    messagesBox.appendChild(wrapper);
    scrollToBottom();
}

function replaceLoadingMessage(content) {
    const loading = document.getElementById("loadingMessage");

    if (loading) {
        loading.remove();
    }

    renderMessage("assistant", content);
}

function clearMessages() {
    messagesBox.innerHTML = "";
}

function scrollToBottom() {
    const chatContainer = document.getElementById("chatContainer");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

async function createNewChat() {
    const user = getUser();

    if (!user) {
        openAuthModal();
        return;
    }

    const chat = await apiRequest("/chat/create", "POST", {
        user_id: user.id
    });

    currentChatId = chat.chat_id;
    localStorage.setItem("sitemind_current_chat", currentChatId);

    clearMessages();
    showWelcomeArea();

    await loadChats();
}

async function loadChats() {
    const user = getUser();

    if (!user) {
        chatList.innerHTML = "";
        return;
    }

    const chats = await apiRequest(`/chat/list/${user.id}`);

    chatList.innerHTML = "";

    chats.forEach(chat => {
        const button = document.createElement("button");

        button.className = `
            w-full text-left px-3 py-3 rounded-lg text-sm mb-1
            hover:bg-[#2b2b2b] transition truncate
            ${Number(currentChatId) === Number(chat.id) ? "bg-[#2b2b2b]" : ""}
        `;

        button.textContent = chat.title || "New Chat";

        button.addEventListener("click", async () => {
            currentChatId = chat.id;
            localStorage.setItem("sitemind_current_chat", currentChatId);
            await loadChatHistory(chat.id);
            await loadChats();
        });

        chatList.appendChild(button);
    });
}

async function loadChatHistory(chatId) {
    const messages = await apiRequest(`/chat/history/${chatId}`);

    clearMessages();

    if (!messages.length) {
        showWelcomeArea();
        return;
    }

    messages.forEach(msg => {
        renderMessage(msg.role, msg.content);
    });
}

async function ensureActiveChat() {
    const user = getUser();

    if (!user) return;

    const savedChatId = localStorage.getItem("sitemind_current_chat");

    await loadChats();

    if (savedChatId) {
        currentChatId = savedChatId;
        await loadChatHistory(currentChatId);
        await loadChats();
        return;
    }

    await createNewChat();
}

async function loadModelOptions() {
    const providerSelect = document.getElementById("providerSelect");
    const modelSelect = document.getElementById("modelSelect");

    const models = await apiRequest("/ai/models");

    function renderModels(provider) {
        modelSelect.innerHTML = "";

        const providerData = models[provider];
        selectedProvider = provider;
        selectedModel = providerData.default;

        providerData.models.forEach(model => {
            const option = document.createElement("option");
            option.value = model.id;
            option.textContent = model.name;
            modelSelect.appendChild(option);
        });

        modelSelect.value = selectedModel;
    }

    providerSelect.addEventListener("change", () => {
        renderModels(providerSelect.value);
    });

    modelSelect.addEventListener("change", () => {
        selectedModel = modelSelect.value;
    });

    renderModels(providerSelect.value);
}

async function sendMessage() {
    const user = getUser();

    if (!user) {
        openAuthModal();
        return;
    }

    const input = document.getElementById("messageInput");
    const question = input.value.trim();

    if (!question) return;

    if (!currentChatId) {
        await createNewChat();
    }

    input.value = "";

    renderMessage("user", question);
    renderLoadingMessage();

    try {
        const response = await apiRequest("/chat/", "POST", {
            chat_id: Number(currentChatId),
            question: question,
            // provider: "ollama",
            // // model: "llama3.1:8b"
            // model: "mistral:latest"
            provider: selectedProvider,
            model: selectedModel
        });

        replaceLoadingMessage(response.answer);
        await loadChats();

    } catch (error) {
        replaceLoadingMessage(`Error: ${error.message}`);
    }
}

newChatBtn.addEventListener("click", createNewChat);