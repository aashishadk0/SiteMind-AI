let currentChatId = null;
let selectedProvider = "ollama";
let selectedModel = "llama3.2:latest";

const chatList = document.getElementById("chatList");
const messagesBox = document.getElementById("messages");
const welcomeScreen = document.getElementById("welcomeScreen");
const newChatBtn = document.getElementById("newChatBtn");
const sidebar = document.getElementById("sidebar");
const sidebarToggleBtn = document.getElementById("sidebarToggleBtn");

function showMessagesArea() {
    welcomeScreen.classList.add("hidden");
    messagesBox.classList.remove("hidden");
}

function showWelcomeArea() {
    welcomeScreen.classList.remove("hidden");
    messagesBox.classList.add("hidden");
}

function createBubble(role, content = "") {
    showMessagesArea();

    const wrapper = document.createElement("div");
    const bubble = document.createElement("div");

    if (role === "user") {
        wrapper.className = "flex justify-end mb-4";
        bubble.className = "max-w-[85%] md:max-w-[75%] rounded-2xl rounded-br-md bg-green-600 px-5 py-3 text-white leading-normal";
    } else {
        wrapper.className = "flex justify-start mb-4";
        bubble.className =
            "markdown-body max-w-[90%] md:max-w-[80%] rounded-2xl rounded-bl-md bg-[#2b2b2b] border border-[#3a3a3a] px-5 py-3 text-gray-100 leading-relaxed";
    }

    bubble.textContent = content.trim();
    wrapper.appendChild(bubble);
    messagesBox.appendChild(wrapper);

    scrollToBottom();
    return bubble;
}

function createWaitingBubble() {
    showMessagesArea();

    const wrapper = document.createElement("div");
    const bubble = document.createElement("div");

    wrapper.className = "flex justify-start mb-4";
    bubble.className = "max-w-[90%] md:max-w-[80%] rounded-2xl rounded-bl-md bg-[#2b2b2b] border border-[#3a3a3a] px-5 py-3 text-gray-300 leading-normal";

    bubble.innerHTML = `
        <div class="flex items-center gap-2">
            <span>Searching knowledge base and preparing answer</span>
            <span class="waiting-dots">
                <span>.</span><span>.</span><span>.</span>
            </span>
        </div>
    `;

    wrapper.appendChild(bubble);
    messagesBox.appendChild(wrapper);

    scrollToBottom();
    return bubble;
}

function renderMessage(role, content) {
    const bubble = createBubble(role, "");

    if (role === "assistant") {
        bubble.classList.add("markdown-body");
        bubble.innerHTML = marked.parse(content.trim());
    } else {
        bubble.textContent = content.trim();
    }
}

function clearMessages() {
    messagesBox.innerHTML = "";
}

function scrollToBottom() {
    const chatContainer = document.getElementById("chatContainer");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function loadModelOptions() {
    const providerSelect = document.getElementById("providerSelect");
    const modelSelect = document.getElementById("modelSelect");

    const models = await apiRequest("/ai/models");
    providerSelect.value = "groq";

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
    closeMobileSidebar();
}

async function deleteChat(chatId) {
    const confirmed = confirm("Delete this chat?");

    if (!confirmed) return;

    await apiRequest(`/chat/delete/${chatId}`, "DELETE");

    if (Number(currentChatId) === Number(chatId)) {
        localStorage.removeItem("sitemind_current_chat");
        currentChatId = null;
        clearMessages();
        showWelcomeArea();
    }

    await loadChats();

    const user = getUser();
    const chats = user ? await apiRequest(`/chat/list/${user.id}`) : [];

    if (!currentChatId && chats.length > 0) {
        currentChatId = chats[0].id;
        localStorage.setItem("sitemind_current_chat", currentChatId);
        await loadChatHistory(currentChatId);
    }
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
        const row = document.createElement("div");

        row.className = `
            group flex items-center gap-2 rounded-lg mb-1 px-2
            hover:bg-[#2b2b2b] transition
            ${Number(currentChatId) === Number(chat.id) ? "bg-[#2b2b2b]" : ""}
        `;

        const button = document.createElement("button");
        button.className = "flex-1 text-left py-3 text-sm truncate";
        button.textContent = chat.title || "New Chat";

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "opacity-70 md:opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-400 transition px-2";
        deleteBtn.innerHTML = "🗑";

        button.addEventListener("click", async () => {
            currentChatId = chat.id;
            localStorage.setItem("sitemind_current_chat", currentChatId);

            await loadChatHistory(chat.id);
            await loadChats();
            closeMobileSidebar();
        });

        deleteBtn.addEventListener("click", async (event) => {
            event.stopPropagation();
            await deleteChat(chat.id);
        });

        row.appendChild(button);
        row.appendChild(deleteBtn);
        chatList.appendChild(row);
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

    const assistantBubble = createWaitingBubble();

    try {
        const response = await fetch("/chat/stream", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                chat_id: Number(currentChatId),
                question: question,
                provider: selectedProvider,
                model: selectedModel
            })
        });

        if (!response.ok) {
            throw new Error("Failed to generate response.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let fullText = "";
        let firstAnswerToken = false;

        while (true) {
            const { value, done } = await reader.read();

            if (done) break;

            const rawChunk = decoder.decode(value);
            const lines = rawChunk.split("\n\n");

            for (const line of lines) {
                if (!line.startsWith("data: ")) continue;

                let token = line.replace("data: ", "");

                if (token === "[DONE]") break;

                token = token.replaceAll("\\n", "\n");

                if (token.includes("Searching knowledge base")) {
                    assistantBubble.textContent = token;
                    continue;
                }

                if (!firstAnswerToken) {
                    assistantBubble.textContent = "";
                    firstAnswerToken = true;
                }

                fullText += token;
                assistantBubble.innerHTML = marked.parse(fullText.trimStart());
                scrollToBottom();
            }
        }

        const finalText = fullText.trim();

        assistantBubble.classList.add("markdown-body");
        assistantBubble.innerHTML = marked.parse(finalText);

        await loadChats();
    } catch (error) {
        assistantBubble.textContent = `Error: ${error.message}`;
    }
}

function openMobileSidebar() {
    sidebar.classList.add("open");
    document.body.classList.add("sidebar-open");
    sidebarToggleBtn.textContent = "×";
}

function closeMobileSidebar() {
    sidebar.classList.remove("open");
    document.body.classList.remove("sidebar-open");
    sidebarToggleBtn.textContent = "☰";
}

function toggleMobileSidebar() {
    if (sidebar.classList.contains("open")) {
        closeMobileSidebar();
    } else {
        openMobileSidebar();
    }
}

sidebarToggleBtn.addEventListener("click", toggleMobileSidebar);

document.addEventListener("click", (event) => {
    const isMobile = window.innerWidth <= 768;
    const clickedSidebar = sidebar.contains(event.target);
    const clickedToggle = sidebarToggleBtn.contains(event.target);

    if (
        isMobile &&
        sidebar.classList.contains("open") &&
        !clickedSidebar &&
        !clickedToggle
    ) {
        closeMobileSidebar();
    }
});

newChatBtn.addEventListener("click", createNewChat);