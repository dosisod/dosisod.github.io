const fs = require('fs');
const hljs = require('highlight.js');

if (process.argv.length != 3) {
  console.error(`usage: ${process.argv[0]} ${process.argv[1]} <language>`);
  process.exit(1);
}

const language = process.argv[2]

const data = fs.readFileSync(process.stdin.fd);

const html = hljs.highlight(data.toString(), {language}).value

console.log(`<pre class="hljs">${html}</pre>`);
