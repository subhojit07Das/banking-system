async function login() {
    const owner = document.getElementById("login-owner").value;
    const pin = document.getElementById("login-pin").value;

    const response = await fetch(
        `/login?account_id=${owner}&pin=${pin}`,
        { method: "POST" }
    );

    const data = await response.json();
       if (data.access_token) {
        document.getElementById("login-result").innerText = 
            `Login Successful`

        localStorage.setItem("token", data.access_token)

        setTimeout(() => {
            window.location.href = "/ui";
        }, 1000);
    }
    else {
        document.getElementById("login-result").innerText = data.error;
    }
}