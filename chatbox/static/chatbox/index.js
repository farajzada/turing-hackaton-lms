let currentChatId = null;

async function sendMessage() {
    const prompt = document.getElementById("prompt").value;
    const model = document.getElementById("model").value;
    const responseDiv = document.getElementById("response");

    responseDiv.innerText = "Göndərilir...";

    const bodyData = {
        prompt,
        model
    };

    // Əgər currentChatId varsa onu da göndər
    if (currentChatId) {
        bodyData.chat_id = currentChatId;
    }

    const res = await fetch("/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bodyData)
    });

    const data = await res.json();
    if (res.ok) {
        responseDiv.innerText += `\n\n${data.response}`;
        currentChatId = data.chat_id; // əgər yeni yaranıbsa onu da saxla
        await loadSession(currentChatId); // cavabı da göstər
        await loadSessions(); // history yenilə
    } else {
        responseDiv.innerText = "Xəta baş verdi: " + (data.error || "Naməlum");
    }

    document.getElementById("prompt").value = "";
}

async function loadSession(chatId) {
    currentChatId = chatId;
    const responseDiv = document.getElementById("response");
    const res = await fetch(`/api/chat/session/${chatId}/`);
    const messages = await res.json();

    responseDiv.innerHTML = messages.map(msg =>
        `<div class="message-block">
            <p><b>🧑 ${msg.prompt}</b><br>🤖 ${msg.response}<br><i>${msg.model}</i> · ${msg.created_at}</p>
            <div class="feedback">
                <button onclick="giveFeedback('like', ${msg.id})">👍</button>
                <button onclick="giveFeedback('dislike', ${msg.id})">👎</button>
            </div>
            <hr>
        </div>`
    ).join("");

    loadSessions();
}

async function loadSessions() {
    const historyDiv = document.getElementById("history");
    const res = await fetch("/api/chat/sessions/");
    const sessions = await res.json();

    historyDiv.innerHTML = sessions.map(s =>
        `<p class="session-item ${s.chat_id === currentChatId ? 'active' : ''}"
            onclick="loadSession('${s.chat_id}')"
            oncontextmenu="showContextMenu(event, '${s.chat_id}')">
            💬 ${s.title}
        </p>`
    ).join("");
}

async function loadLatestSession() {
    const res = await fetch("/api/chat/sessions/");
    const sessions = await res.json();
    if (sessions.length > 0) {
        await loadSession(sessions[0].chat_id);
    }
}

function newChat() {
    currentChatId = null;
    document.getElementById("response").innerHTML = "";
    document.getElementById("prompt").value = "";
}

window.onload = () => {
    loadSessions();
};

let contextMenu = document.getElementById("context-menu");
let clickedChatId = null;

document.addEventListener("click", () => {
    contextMenu.style.display = "none";
});

function showContextMenu(event, chatId) {
    event.preventDefault();
    clickedChatId = chatId;
    contextMenu.style.top = event.pageY + "px";
    contextMenu.style.left = event.pageX + "px";
    contextMenu.style.display = "block";
}

async function renameChat() {
    const newTitle = prompt("Yeni başlığı yaz:");
    if (newTitle) {
        await fetch(`/api/chat/session/${clickedChatId}/rename/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: newTitle })
        });
        loadSessions();
    }
    contextMenu.style.display = "none";
}

async function deleteChat() {
    await fetch(`/api/chat/session/${clickedChatId}/delete/`, {
        method: "DELETE"
    });
    loadSessions();
    document.getElementById("response").innerHTML = "";
    contextMenu.style.display = "none";
}

responseDiv.innerHTML = messages.map(msg =>
    `<div class="message-block">
        <p><b>🧑 ${msg.prompt}</b><br>🤖 ${msg.response}<br><i>${msg.model}</i> · ${msg.created_at}</p>
        <div class="feedback">
            <button onclick="giveFeedback('like', ${msg.id})">👍</button>
            <button onclick="giveFeedback('dislike', ${msg.id})">👎</button>
        </div>
        <hr>
    </div>`
).join("");


async function giveFeedback(feedback, messageId) {
    const res = await fetch(`/api/chat/message/${messageId}/feedback/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feedback })
    });

    if (res.ok) {
        alert("Rəyiniz qeydə alındı!");
    } else {
        alert("Rəy göndərilə bilmədi.");
    }
}