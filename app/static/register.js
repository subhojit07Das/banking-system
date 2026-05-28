async function createAccount() {
    const owner = document.getElementById("register-owner").value;
    const balance = document.getElementById("register-balance").value;
    const pin = document.getElementById("register-pin").value;

    const response = await fetch(
        `/accounts?owner=${owner}&initial_balance=${balance}&pin=${pin}`,
        { method: "POST" }
    );

    const data = await response.json();
    if (data.id) {
        document.getElementById("register-result").innerText = 
            `Account Created! Your ID is ${data.id}. Save this!`

        setTimeout(() => {
            window.location.href = "/login";
        }, 1000);
    }
    else {
        document.getElementById("register-result").innerText = data.error;
    }
}