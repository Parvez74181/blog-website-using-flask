const user_name = document.querySelector("#user-name");
const user_address = document.querySelector("#user-address");
const user_email = document.querySelector("#user-email");
const user_password = document.querySelector("#user-password");
const user_confirm_password = document.querySelector("#user-confirm-password");
const registration_form = document.querySelector(".registration-form");
const email_err = document.querySelector(".email-err");
const pass_err = document.querySelectorAll(".pass-err");
const fa_eye = document.querySelectorAll(".fa-eye");
const fa_eye_slash = document.querySelectorAll(".fa-eye-slash");

// change input type password to text
fa_eye.forEach((item, i) => {
  item.addEventListener("click", () => {
    item.style.display = "none";
    fa_eye_slash[i].style.display = "block";
    if (i === 0) user_password.type = "text";
    if (i === 1) user_confirm_password.type = "text";
  });
});

// change input type text to password
fa_eye_slash.forEach((item, i) => {
  item.addEventListener("click", () => {
    item.style.display = "none";
    fa_eye[i].style.display = "block";
    if (i === 0) user_password.type = "password";
    if (i === 1) user_confirm_password.type = "password";
  });
});

registration_form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (user_password.value !== user_confirm_password.value) {
    msg = `password doesn't matched!`;
    pass_err.forEach((item) => {
      item.innerText = msg;
    });
  } else {
    try {
      let res = await axios.post("/registration", {
        user_name: user_name.value,
        user_address: user_address.value,
        user_email: user_email.value,
        user_password: user_password.value,
      });

      if (res.status === 201) window.location.pathname = "/login";
    } catch (e) {
      email_err.innerText = e.response.data.message;
    }
  }
});

// console.log((window.location.pathname = "/"));
