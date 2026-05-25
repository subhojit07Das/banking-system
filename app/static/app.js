async function createAccount() {
    const owner = document.getElementById("owner").value;
    const balance = document.getElementById("balance").value;
    const pin = document.getElementById("pin").value;

    const response = await fetch(
        `/accounts?owner=${owner}&initial_balance=${balance}&pin=${pin}`,
        { method: "POST" }
    );

    const data = await response.json();
    document.getElementById("create-result").innerText = JSON.stringify(data);
}

async function getHistory() {
    const owner = document.getElementById("history-account-id").value;
    const pin = document.getElementById("history-pin").value;

    const response = await fetch (
        `/accounts/${owner}/history?pin=${pin}`,
        { method: "GET"}
    );

    const data = await response.json();
    document.getElementById("history-result").innerText = JSON.stringify(data);
}

async function getAccount() {
    const owner = document.getElementById("get-account-id").value;
    const pin = document.getElementById("get-password").value;

    const response = await fetch (
        `/accounts/${owner}?pin=${pin}`,
        { method: "GET" }
    )

    const data = await response.json();
    document.getElementById("get-result").innerText = JSON.stringify(data);
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
    document.getElementById("deposit-result").innerText = JSON.stringify(data);
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
    document.getElementById("withdraw-result").innerText = JSON.stringify(data);
};