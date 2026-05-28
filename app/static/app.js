async function getHistory() {
    const owner = document.getElementById("history-account-id").value;
    const pin = document.getElementById("history-pin").value;

    const response = await fetch (
        `/accounts/${owner}/history?pin=${pin}`,
        { method: "GET"}
    );

    const data = await response.json();
    if (data.history) {
    let result = "Transaction History:\n\n";
    data.history.forEach(t => {
        result += `${t.type.toUpperCase()} | Amount: ${parseFloat(t.amount).toFixed(2)} | Balance after: ${parseFloat(t.balance_after).toFixed(2)}\n`;
});
    
    document.getElementById("history-result").innerText = result;

    setTimeout(() => {
        location.reload();
    }, 5000);

    }
    else {
        document.getElementById("history-result").innerText = data.error;
    }
}

async function getAccount() {
    const owner = document.getElementById("get-account-id").value;
    const pin = document.getElementById("get-password").value;

    const response = await fetch (
        `/accounts/${owner}?pin=${pin}`,
        { method: "GET" }
    )

    const data = await response.json();
    if (data.id) {
    document.getElementById("get-result").innerText = 
        `Owner: ${data.owner} | Balance: ${data.balance}`
    
    setTimeout(() => {
        location.reload();
    }, 5000);

    }
    else {
        document.getElementById("get-result").innerText = data.error;
    }
}; 

async function deposit() {
    const owner = document.getElementById("deposit-account-id").value;
    const amount = document.getElementById("deposit-amount").value;
    const pin = document.getElementById("deposit-pin").value;

    const response = await fetch (
        `/accounts/${owner}/deposit?amount=${amount}&pin=${pin}`,
        { method: "POST" }
    ) 

    const data = await response.json();
    if (data.message) {
        document.getElementById("deposit-result").innerText = 
            `Deposit Successful! New Balance: ${data.balance}`

        setTimeout(() => {
            document.getElementById("deposit-result").innerText = "";
            location.reload();
        }, 5000)

        document.getElementById("deposit-account-id").value = "";
        document.getElementById("deposit-amount").value = "";
        document.getElementById("deposit-pin").value = "";
    }
    else {
        document.getElementById("deposit-result").innerText = data.error;
    }
};

async function withdraw() {
    const owner = document.getElementById("withdraw-account-id").value;
    const amount = document.getElementById("withdraw-amount").value;
    const pin = document.getElementById("withdraw-pin").value;

    const response = await fetch (
        `/accounts/${owner}/withdraw?amount=${amount}&pin=${pin}`,
        { method: "POST" }
    ) 

    const data = await response.json();
    if (data.message) {
        document.getElementById("withdraw-result").innerText = 
            `Withdrawl Successful! New Balance: ${data.balance}`

        setTimeout(() => {
            document.getElementById("withdraw-result").innerText = "";
            location.reload();
        }, 5000)

        document.getElementById("withdraw-account-id").value = "";
        document.getElementById("withdraw-amount").value = "";
        document.getElementById("withdraw-pin").value = "";
    }
    else {
        document.getElementById("withdraw-result").innerText = data.error;
    }
};

async function transfer() {
    const sender = document.getElementById("transfer-sender-id").value;
    const receiver = document.getElementById("transfer-receiver-id").value;
    const amount = document.getElementById("transfer-amount").value;
    const pin = document.getElementById("transfer-password").value;

    const response = await fetch (
        `/accounts/${sender}/transfer?receiver_id=${receiver}&amount=${amount}&pin=${pin}`,
        { method: "POST" }
    )

    const data = await response.json();
    if (data.message) {
        document.getElementById("transfer-result").innerText = data.message;

        setTimeout(() => {
            document.getElementById("transfer-result").innerText = "";
            location.reload();
        }, 5000)

        document.getElementById("transfer-sender-id").value = "";
        document.getElementById("transfer-receiver-id").value = "";
        document.getElementById("transfer-amount").value = "";
        document.getElementById("transfer-password").value = "";
    }
    else {
        document.getElementById("transfer-result").innerText = data.error;
    }
};


async function closeAccount() {
    const owner = document.getElementById("close-account-id").value;
    const pin = document.getElementById("close-password").value;

    const response = await fetch (
        `/accounts/${owner}?pin=${pin}`,
        { method: "DELETE" }
    );

    const data = await response.json();
    if (data.message) {
        document.getElementById("close-result").innerText = data.message;

        setTimeout(() => {
            document.getElementById("close-result").innerText = "";
            location.reload();
        }, 5000)

        document.getElementById("close-account-id").value = "";
        document.getElementById("close-password").value = "";
    }
    else {
        document.getElementById("close-result").innerText = data.error;
    }
}