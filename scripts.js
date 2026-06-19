async function sendMessage() {

    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const userText = input.value.trim();

    if(userText === "") return;

    const userMsg = document.createElement("div");

    userMsg.classList.add("message","user");

    userMsg.innerText = userText;

    chatBox.appendChild(userMsg);

    input.value = "";

    const typing = document.createElement("div");

    typing.classList.add(
        "message",
        "bot",
        "typing"
    );

    typing.innerText = "🤖 Thinking...";

    chatBox.appendChild(typing);

    chatBox.scrollTop = chatBox.scrollHeight;

    try{

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    message:userText
                })
            }
        );

        const data = await response.json();

        typing.remove();

        const botMsg = document.createElement("div");

        botMsg.classList.add(
            "message",
            "bot"
        );

        botMsg.innerText = data.response;

        chatBox.appendChild(botMsg);

    }
    catch(error){

        typing.remove();

        const errorMsg = document.createElement("div");

        errorMsg.classList.add(
            "message",
            "bot"
        );

        errorMsg.innerText =
        "❌ Unable to connect to FastAPI server.";

        chatBox.appendChild(errorMsg);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

document
.getElementById("user-input")
.addEventListener(
    "keypress",
    function(e){

        if(e.key === "Enter"){
            sendMessage();
        }
    }
);