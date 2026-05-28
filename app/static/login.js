async function login() {
    const owner = document.getElementById("login-owner").value;
    const pin = document.getElementById("login-pin").value;

    const response = await fetch(
        `/accounts/${owner}?pin=${pin}`,
        { method: "GET" }
    );

    const data = await response.json();
       if (data.id) {
        document.getElementById("login-result").innerText = 
            `Login Successful`

        setTimeout(() => {
            window.location.href = "/ui";
        }, 3000);
    }
    else {
        document.getElementById("login-result").innerText = data.error;
    }
}