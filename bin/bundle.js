function nu(e,n,t,r){if(!n)return document.getElementById(e);let o=document.createElement(e);if(n)for(const e in n)o[e]=n[e];let d=o;if(t){let e=[];Array.isArray(t)?e=t:e.push(t),e.forEach((function(e){var n;(n=e)instanceof HTMLElement?o=n.appendChild(o).parentNode:"string"==typeof n&&(o=document.getElementById(n).appendChild(o).parentNode)}))}return r?d:o}
function recent_commits(){fetch("https://api.github.com/users/dosisod/events").then((function(e){return e.json()})).then((function(e){parse_events(e)}))}function parse_events(e){var t=[];for(const n of e){const e=new Date(n.created_at).toString().split(" ").splice(1,2).join(" "),s=n.repo.name.split("/")[1];if("PushEvent"==n.type)for(const a of n.payload.commits.reverse())t.push({date:e,commit_msg:a.message.replace(/\n/g," "),repo:s});else"CreateEvent"==n.type&&null==n.payload.ref?t.push({date:e,new:"new repo",repo:s}):"PullRequestEvent"==n.type&&"closed"==n.payload.pull_request.state&&t.push({date:e,new:"new PR",repo:s})}var n="";for(const e of t){const t=nu("li",{className:"recent-commit"});let s="bubble-fill";e.date==n&&(s="bubble-spacer"),addspan(e.date,s,t),n=e.date,s="bubble-void",addspan(e.repo,s,t),(e.commit_msg||e.new)&&(e.new&&(s="bubble-fill"),addspan(e.commit_msg||e.new,s,t),nu("recent").appendChild(t))}}function addspan(e,t,n){nu("span",{className:"bubble "+t,innerText:e},n)}
