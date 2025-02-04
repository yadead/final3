if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}

// This script toggles the active class and aria-current attribute on the nav links
document.addEventListener("DOMContentLoaded", function () {
  const navLinks = document.querySelectorAll(".nav-link");
  const currentUrl = window.location.pathname;

  navLinks.forEach((link) => {
    const linkUrl = link.getAttribute("href");
    if (linkUrl === currentUrl) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});


  function signIn() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    alert("Signing in as: " + username);
    // You can also send this data to the server here
  }

  function signUp() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => alert(data.message)) // Show the server response
    .catch(error => console.error("Error:", error)); // Log any errors
  }

  function submit() {
    // Prevent form submission if inside a form
    event.preventDefault(); 

    let Project = document.getElementById("Project").value;
    let Start_Time = document.getElementById("Start_Time").value;
    let End_Time = document.getElementById("End_Time").value;
    let Repo = document.getElementById("Repo").value;
    let Developer_Notes = document.getElementById("Developer_Notes").value;

    console.log({
      Project: Project,
      Start_Time: Start_Time,
      End_Time: End_Time,
      Repo: Repo,
      Developer_Notes: Developer_Notes
    });

    // You can send the data to the server or handle it further here
  }

