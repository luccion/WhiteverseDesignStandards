const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 5454;

app.use(express.static("public"));
app.use("/images", express.static("Images"));
// 中间件来解析请求体
app.use(express.json());

// 定义首页路由
app.get("/", (req, res) => {
  // 假设 index.html 在项目根目录下
  res.sendFile(path.join(__dirname, "index.html"));
});

app.post("/get-readme", (req, res) => {
  const readmePath = path.join(__dirname, "README.md");
  fs.readFile(readmePath, "utf8", (err, data) => {
    if (err) {
      console.error(err);
      return res.status(500).send("Error reading README.md file");
    }
    res.send(data);
  });
});

(async () => {
  const open = (await import("open")).default;
  app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
    open(`http://localhost:${port}`);
  });
})();
