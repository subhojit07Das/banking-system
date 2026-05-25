async function createAccount() {
    const owner = document.getElementById("owner").value;
    const balance = document.getElementById("balance").value;
    const pin = document.getElementById("pin").value;

    const response = await fetch(
        `/accounts?owner=${owner}&initial_balance=${balance}&pin=${pin}`,
        { method: "POST" }
    );

    const data = await response.json();
    if (data.id) {
        document.getElementById("create-result").innerText = 
            `Account Created! Your ID is ${data.id}. Save this!`

        document.getElementById("owner").value = "";
        document.getElementById("balance").value = "";
        document.getElementById("pin").value = "";
    }
    else {
        document.getElementById("create-result").innerText = data.error;
    }
}

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
            result += `${t.type.toUpperCase()} | Amount: ${t.amount} | Balance after: ${t.balance_after}\n`;
        });
    document.getElementById("history-result").innerText = result;
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

        document.getElementById("withdraw-account-id").value = "";
        document.getElementById("withdraw-amount").value = "";
        document.getElementById("withdraw-pin").value = "";
    }
    else {
        document.getElementById("withdraw-result").innerText = data.error;
    }
};