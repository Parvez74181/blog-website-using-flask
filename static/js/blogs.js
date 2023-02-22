let blog_container = document.querySelector(".blogs .blog-container");

const fetchBlog = async () => {
  let res = await axios.get("/fetch_blogs");
  if (res.status === 200) {
    res.data.forEach((data) => {
      let html = `
      <div class="card">
        <img loading="lazy" src="data:image/png;base64,${data.thumbnail}" class="card-img-top rounded" alt="...">
                <div class="card-body">
                      <a href="/blog/${data.title}/${data.id}" style="text-decoration:none;color:rgb(163, 163, 163);"><h5 class="card-title flex">${data.title}</h5></a>
                      <p class="card-text flex">${data.description}</p>
                      <a href="/blog/${data.title}/${data.id}" class="btn">Read More</a>
                </div>
       </div>
      `;
      blog_container.insertAdjacentHTML("afterbegin", html);
    });
  }
};

fetchBlog();
