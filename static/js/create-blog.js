const blog_upload_form = document.querySelector(".blog-upload-form");
const img_input = blog_upload_form.querySelector("#thumbnail-image");
const title = blog_upload_form.querySelector("#post-title");
const description = blog_upload_form.querySelector("#post-desc");
const submit_btn = blog_upload_form.querySelector("#submit-btn");

let img_uri;
img_input.addEventListener("change", (e) => {
  img_uri = e.target.files[0];
});

if (submit_btn.innerText == "Upload Blog") {
  blog_upload_form.addEventListener("submit", async (e) => {
    try {
      e.preventDefault();
      const formData = new FormData();
      formData.append("file", img_uri);
      formData.append("title", title.value);
      formData.append("description", description.value);
      let res = await axios.post("/create/blog", formData);

      if (res.status === 201) window.location.pathname = "/blogs";
    } catch (e) {
      console.log(e);
    }
  });
} else if (submit_btn.innerText == "Update Blog") {
  let path = window.location.pathname.split("/");

  blog_upload_form.addEventListener("submit", async (e) => {
    try {
      e.preventDefault();
      const formData = new FormData();
      formData.append("title", title.value);
      formData.append("description", description.value);
      let res = await axios.post(`/update/${path[2]}/${path[3]}`, formData);
      if (res.status === 200) window.location.pathname = "/blogs";
    } catch (e) {
      console.log(e);
    }
  });
}
