(function() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/login";
    }
})();

const token = localStorage.getItem("token");

async function getHistory() {
    const owner = document.getElementById("history-account-id").value;

    const response = await fetch(
        `/accounts/${owner}/history`,
        { 
            method: "GET", 
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();
    if (data.history) {
        let result = "Transaction History:\n\n";
        data.history.forEach(t => {
            result += `${t.type.toUpperCase()} | Amount: ${Number(t.amount).toFixed(2)} | Balance after: ${Number(t.balance_after).toFixed(2)}\n`;
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

    const response = await fetch(
        `/accounts/${owner}`,
        { 
            method: "GET", 
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();
    if (data.id) {
        document.getElementById("get-result").innerText = 
            `Owner: ${data.owner} | Balance: ${Number(data.balance).toFixed(2)}`;
        
        setTimeout(() => {
            location.reload();
        }, 5000);
    }
    else {
        document.getElementById("get-result").innerText = data.error;
    }
}

async function deposit() {
    const owner = document.getElementById("deposit-account-id").value;
    const amount = document.getElementById("deposit-amount").value;

    const response = await fetch(
        `/accounts/${owner}/deposit?amount=${amount}`,
        { 
            method: "POST", 
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();
    if (data.message) {
        document.getElementById("deposit-result").innerText = 
            `Deposit Successful! New Balance: ${Number(data.balance).toFixed(2)}`;

        setTimeout(() => {
            document.getElementById("deposit-result").innerText = "";
            location.reload();
        }, 5000);

        document.getElementById("deposit-account-id").value = "";
        document.getElementById("deposit-amount").value = "";
    }
    else {
        document.getElementById("deposit-result").innerText = data.error;
    }
}

async function withdraw() {
    const owner = document.getElementById("withdraw-account-id").value;
    const amount = document.getElementById("withdraw-amount").value;

    const response = await fetch(
        `/accounts/${owner}/withdraw?amount=${amount}`,
        { 
            method: "POST", 
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();
    if (data.message) {
        document.getElementById("withdraw-result").innerText = 
            `Withdrawal Successful! New Balance: ${Number(data.balance).toFixed(2)}`;

        setTimeout(() => {
            document.getElementById("withdraw-result").innerText = "";
            location.reload();
        }, 5000);

        document.getElementById("withdraw-account-id").value = "";
        document.getElementById("withdraw-amount").value = "";
    }
    else {
        document.getElementById("withdraw-result").innerText = data.error;
    }
}

async function transfer() {
    const sender = document.getElementById("transfer-sender-id").value;
    const receiver = document.getElementById("transfer-receiver-id").value;
    const amount = document.getElementById("transfer-amount").value;

    const response = await fetch(
        `/accounts/${sender}/transfer?receiver_id=${receiver}&amount=${amount}`,
        { 
            method: "POST", 
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();
    if (data.message) {
        document.getElementById("transfer-result").innerText = data.message;

        setTimeout(() => {
            document.getElementById("transfer-result").innerText = "";
            location.reload();
        }, 5000);

        document.getElementById("transfer-sender-id").value = "";
        document.getElementById("transfer-receiver-id").value = "";
        document.getElementById("transfer-amount").value = "";
    }
    else {
        document.getElementById("transfer-result").innerText = data.error;
    }
}

async function closeAccount() {
    const owner = document.getElementById("close-account-id").value;

    const response = await fetch(
        `/accounts/${owner}`,
        { 
            method: "DELETE", 
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    const data = await response.json();
    if (data.message) {
        document.getElementById("close-result").innerText = data.message;

        setTimeout(() => {
            document.getElementById("close-result").innerText = "";
            localStorage.removeItem("token");
            window.location.href = "/login";
        }, 5000);

        document.getElementById("close-account-id").value = "";
    }
    else {
        document.getElementById("close-result").innerText = data.error;
    }
}