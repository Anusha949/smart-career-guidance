document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");

  loginForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    // Dummy check
    if (username === "admin" && password === "password123") {
      window.location.href = "index.html";
    } else {
      alert("Invalid username or password");
    }
  });
});
