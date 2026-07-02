console.log("SiteMind AI frontend loaded");

const sendBtn = document.getElementById("sendBtn");
const messageInput = document.getElementById("messageInput");

sendBtn.addEventListener("click", sendMessage);

messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

document.addEventListener("DOMContentLoaded", async () => {
    updateAuthUI();

    await loadModelOptions();

    if (getUser()) {
        await ensureActiveChat();
    }
});