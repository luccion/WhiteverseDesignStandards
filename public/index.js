(async function () {
  const documentation = await post();
  if (!documentation) return;

  const $ = (selector) => document.querySelector(selector);
  $("#DocContent").innerHTML = parseContent(documentation);
  $("#DocNavigator").innerHTML = parseNavigation(documentation);
  const scrollSpy = new bootstrap.ScrollSpy($("#DocContent"), {
    target: "#DocNavigator",
  });

  const images = document.querySelectorAll(".clickable-image");
  images.forEach((image) => {
    // 初始化每个图片的状态
    image.dataset.maxed = "false"; // 使用数据属性来标记是否放大
    // 根据图片原始大小设置初始最大宽度和鼠标样式
    if (image.naturalWidth > 300) {
      image.style.maxWidth = "300px";
      image.style.cursor = "zoom-in";
    } else {
      image.style.cursor = "default";
    }

    image.addEventListener("click", () => {
      if (image.dataset.maxed === "false") {
        image.dataset.maxed = "true";
        image.style.maxWidth = "none"; // 放大图片
        image.style.cursor = "zoom-out";
      } else {
        image.dataset.maxed = "false";
        image.style.maxWidth = "300px"; // 缩小图片
        image.style.cursor = "zoom-in";
      }
    });
  });

  function parseContent(content) {
    const renderer = new marked.Renderer();
    renderer.heading = (text, level) => {
      const anchorId = text.toLowerCase().replace(/[^\S\r\n]+/g, "-");
      return `<h${level} id="doc.${anchorId}"><a class="header-link" href="#doc.${anchorId}">${text}</a></h${level}>`;
    };
    renderer.image = (href) => {
      return `<img class="clickable-image" src="${href}"/>`;
    };

    marked.use({ renderer });
    return marked.parse(content);
  }
  function parseNavigation(content) {
    const renderer = new marked.Renderer();
    const navigationItems = [];
    renderer.heading = (text, level) => {
      if (level < 5) {
        const indent = "  ".repeat(level - 1);
        const anchorId = text.toLowerCase().replace(/[^\S\r\n]+/g, "-");
        const className = `doc-nav-${"i".repeat(level)}`;
        navigationItems.push(
          `${indent}<li><a class="doc-nav ${className}" href="#doc.${anchorId}">${text}</a></li>`
        );
        return `<h${level} id="${anchorId}">${text}</h${level}>`;
      } else {
        return ``;
      }
    };
    marked.use({ renderer });
    marked.parse(content);
    return `<ul>${navigationItems.join("")}</ul>`;
  }

  async function post() {
    try {
      const response = await fetch("get-readme", {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      return response.text();
    } catch (error) {
      console.error("Error:", error);
    }
  }
})();
