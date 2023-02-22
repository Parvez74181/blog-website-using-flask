const login_form = document.querySelector(".login-form");
const user_email = document.querySelector("#user-email");
const user_password = document.querySelector("#user-password");
const fa_eye = document.querySelector(".fa-eye");
const fa_eye_slash = document.querySelector(".fa-eye-slash");

// change input type password to text
fa_eye.addEventListener("click", () => {
  fa_eye.style.display = "none";
  fa_eye_slash.style.display = "block";
  user_password.type = "text";
});

// change input type text to password
fa_eye_slash.addEventListener("click", () => {
  fa_eye_slash.style.display = "none";
  fa_eye.style.display = "block";
  user_password.type = "password";
});

login_form.addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    let res = await axios.post("/login", {
      user_email: user_email.value,
      user_password: user_password.value,
    });
    if (res.status === 200) window.location.pathname = "/";
  } catch (e) {
    console.log(e.response.data.message);
  }
});
