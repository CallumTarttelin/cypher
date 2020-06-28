document.getElementById("submit").addEventListener("click", (_) => {
    const value = document.getElementById("answer").value;
    const path = window.location.pathname;
    const submitPath = path.replace("view", "submit");
    fetch(submitPath, { method: 'POST', redirect: 'follow', body: value })
        .then(async response => {
            if (response.status === 200 && ! response.redirected) {
                const data = await response.json();
                document.getElementById("message").textContent = data.message;
                document.getElementById("message").className = data.status;
            } else if (response.status === 200 && response.redirected) {
                window.location.href = response.url;
            }
        })
        .catch(err => console.error(err));
});
