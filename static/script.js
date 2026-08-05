async function sendMessage(){

    let input=document.getElementById("question");

    let question=input.value;

    if(question==="") return;

    let chat=document.getElementById("chat-box");

    chat.innerHTML+=`
    <div class="user">
        <span>${question}</span>
    </div>
    `;

    input.value="";

    let response=await fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            question:question
        })

    });

    let data=await response.json();

    chat.innerHTML+=`
    <div class="bot">
        <span>${data.answer}</span>
    </div>
    `;

    chat.scrollTop=chat.scrollHeight;
}