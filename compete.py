"""
compete.py — Competition Mode for OpenEnv Data Pipeline Debugger
Side-by-side agent battle with graphs. UI matches dashboard theme.
"""

from __future__ import annotations


def get_compete_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenEnv — Agent Arena</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f9fafb; --text-color: #111827; --text-muted: #6b7280;
            --border-color: #e5e7eb; --primary-color: #2563eb; --primary-hover: #1d4ed8;
            --bg-card: #ffffff; --success: #059669; --danger: #dc2626; --navbar-height: 56px;
        }
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg-color); color: var(--text-color); line-height: 1.5; }

        /* ── Navbar (matches dashboard) ── */
        .topnav { position:fixed; top:0; left:0; right:0; height:var(--navbar-height); background:#0f172a; border-bottom:1px solid #1e293b; display:flex; align-items:center; padding:0 1.5rem; z-index:1000; box-shadow:0 2px 8px rgba(0,0,0,0.25); }
        .topnav-brand { display:flex; align-items:center; gap:0.6rem; font-weight:700; font-size:0.95rem; color:#f1f5f9; text-decoration:none; margin-right:2rem; }
        .topnav-brand .logo-dot { width:8px; height:8px; background:#6366f1; border-radius:50%; }
        .topnav-links { display:flex; align-items:center; gap:0.25rem; flex:1; }
        .topnav-link { display:flex; align-items:center; gap:0.4rem; padding:0.4rem 0.85rem; border-radius:6px; color:#94a3b8; text-decoration:none; font-size:0.85rem; font-weight:500; transition:background 0.18s,color 0.18s; }
        .topnav-link:hover { background:rgba(255,255,255,0.07); color:#f1f5f9; }
        .topnav-link.active { background:rgba(99,102,241,0.18); color:#818cf8; }
        .topnav-divider { width:1px; height:20px; background:#1e293b; margin:0 0.5rem; }
        .topnav-status { display:flex; align-items:center; gap:0.5rem; font-size:0.78rem; font-weight:500; margin-left:auto; }
        .status-dot { width:7px; height:7px; border-radius:50%; background:#334155; transition:background 0.3s; }
        .status-dot.online { background:#10b981; box-shadow:0 0 6px #10b981; }

        /* ── Page ── */
        .page-wrapper { margin-top: var(--navbar-height); padding: 2rem 3rem; max-width: 1300px; margin-left: auto; margin-right: auto; }
        .page-title { display:flex; justify-content:space-between; align-items:center; margin-bottom:2rem; padding-bottom:1rem; border-bottom:1px solid var(--border-color); }
        .page-title h2 { font-size:1.5rem; font-weight:600; }

        /* ── Cards ── */
        .card { background:var(--bg-card); border:1px solid var(--border-color); border-radius:6px; padding:1.5rem; margin-bottom:1.5rem; box-shadow:0 1px 2px rgba(0,0,0,0.05); }
        .card-header { font-weight:600; margin-bottom:1rem; font-size:1rem; }

        /* ── Controls ── */
        .ctrl-group { display:flex; gap:1rem; align-items:center; flex-wrap:wrap; }
        select, button { padding:0.5rem 1rem; border:1px solid var(--border-color); border-radius:4px; font-size:0.9rem; font-family:inherit; }
        button { background:var(--bg-card); cursor:pointer; font-weight:500; transition:0.2s; }
        button:hover { background:var(--bg-color); }
        button.primary { background:var(--primary-color); color:white; border-color:var(--primary-color); }
        button.primary:hover { background:var(--primary-hover); }
        button:disabled { opacity:0.5; cursor:not-allowed; }

        /* ── Scoreboard ── */
        .scoreboard { display:grid; grid-template-columns:1fr auto 1fr; gap:0; margin-bottom:1.5rem; background:var(--bg-card); border:1px solid var(--border-color); border-radius:6px; overflow:hidden; }
        .score-side { display:flex; flex-direction:column; align-items:center; padding:1.25rem; gap:0.3rem; }
        .score-agent { font-size:0.75rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; }
        .score-agent.blue { color: var(--primary-color); }
        .score-agent.green { color: var(--success); }
        .score-val { font-size:2rem; font-weight:700; font-variant-numeric:tabular-nums; }
        .score-val.blue { color: var(--primary-color); }
        .score-val.green { color: var(--success); }
        .score-meta { font-size:0.75rem; color:var(--text-muted); }
        .score-divider { display:flex; align-items:center; justify-content:center; padding:0 1.25rem; border-left:1px solid var(--border-color); border-right:1px solid var(--border-color); }
        .vs-badge { width:40px; height:40px; border-radius:50%; background:linear-gradient(135deg,#2563eb,#059669); display:flex; align-items:center; justify-content:center; font-size:0.7rem; font-weight:700; color:#fff; }

        /* ── Arena grid ── */
        .arena { display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; margin-bottom:1.5rem; }
        .agent-header { display:flex; align-items:center; gap:0.65rem; margin-bottom:1rem; padding-bottom:0.75rem; border-bottom:2px solid var(--border-color); }
        .agent-header.blue { border-bottom-color: var(--primary-color); }
        .agent-header.green { border-bottom-color: var(--success); }
        .agent-icon { width:32px; height:32px; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:1.1rem; }
        .agent-icon.blue { background:rgba(37,99,235,0.1); }
        .agent-icon.green { background:rgba(5,150,105,0.1); }
        .agent-name { font-weight:600; font-size:0.9rem; }
        .agent-desc { font-size:0.75rem; color:var(--text-muted); }

        /* ── Log ── */
        .log-panel { max-height:350px; overflow-y:auto; border:1px solid var(--border-color); border-radius:4px; }
        .log-entry { padding:0.6rem 0.75rem; border-bottom:1px solid var(--border-color); font-size:0.82rem; display:flex; justify-content:space-between; align-items:flex-start; gap:0.5rem; }
        .log-entry:last-child { border-bottom:none; }
        .log-action { font-weight:600; }
        .log-desc { color:var(--text-muted); font-size:0.75rem; margin-top:0.15rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:250px; }
        .log-reward { font-weight:600; white-space:nowrap; font-size:0.82rem; }
        .pos { color: var(--success); }
        .neg { color: var(--danger); }
        .neu { color: var(--text-muted); }
        .log-empty { padding:2rem; text-align:center; color:var(--text-muted); font-size:0.85rem; }

        /* ── Winner ── */
        .winner-banner { display:none; padding:1rem; text-align:center; border-radius:6px; margin-bottom:1.5rem; font-weight:600; }
        .winner-banner.show { display:block; animation: fadeIn 0.4s ease; }
        .winner-banner.blue-win { background:rgba(37,99,235,0.08); border:1px solid rgba(37,99,235,0.2); color:var(--primary-color); }
        .winner-banner.green-win { background:rgba(5,150,105,0.08); border:1px solid rgba(5,150,105,0.2); color:var(--success); }
        .winner-banner.tie-win { background:rgba(245,158,11,0.08); border:1px solid rgba(245,158,11,0.2); color:#d97706; }

        /* ── Charts ── */
        .charts-grid { display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; }

        @keyframes fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
        @media(max-width:768px) { .arena,.charts-grid { grid-template-columns:1fr; } .page-wrapper { padding:1rem; } }
    </style>
</head>
<body>

<nav class="topnav">
    <a class="topnav-brand" href="/"><span class="logo-dot"></span> OpenEnv Debugger</a>
    <div class="topnav-links">
        <a class="topnav-link" href="/dashboard"><span>📊</span> Dashboard</a>
        <a class="topnav-link" href="/demo"><span>🎬</span> Demo</a>
        <a class="topnav-link active" href="/compete"><span>⚔️</span> Compete</a>
        <div class="topnav-divider"></div>
        <a class="topnav-link" href="/docs" target="_blank"><span>📖</span> API Docs</a>
        <a class="topnav-link" href="/tasks" target="_blank"><span>📋</span> Tasks</a>
        <a class="topnav-link" href="/health" target="_blank"><span>🩺</span> Health</a>
    </div>
    <div class="topnav-status">
        <span class="status-dot" id="navDot"></span>
        <span id="navStatus" style="color:#94a3b8">Connecting...</span>
    </div>
</nav>

<div class="page-wrapper">

    <div class="page-title">
        <h2>⚔️ Competition Arena</h2>
        <span style="font-size:0.85rem;color:var(--text-muted)">Two agents. One task. Real independent execution.</span>
    </div>

    <!-- Controls -->
    <div class="card">
        <div class="ctrl-group">
            <select id="taskSelect">
                <option value="task_easy_schema_fix">Easy — Schema Fix</option>
                <option value="task_medium_data_quality">Medium — Data Quality</option>
                <option value="task_hard_pipeline_orchestration">Hard — Pipeline Orchestration</option>
                <option value="task_veryhard_streaming_pipeline">Very Hard — Streaming Pipeline</option>
                <option value="task_expert_multi_source_join">Expert — Multi-Source Join</option>
            </select>
            <button class="primary" id="runBtn" onclick="startBattle()">▶ Start Battle</button>
            <span id="progText" style="font-size:0.85rem;color:var(--text-muted)"></span>
        </div>
    </div>

    <!-- Winner Banner -->
    <div class="winner-banner" id="winnerBanner"></div>

    <!-- Scoreboard -->
    <div class="scoreboard">
        <div class="score-side">
            <div class="score-agent blue">Fixed Strategy</div>
            <div class="score-val blue" id="score1">—</div>
            <div class="score-meta" id="meta1">awaiting</div>
        </div>
        <div class="score-divider"><div class="vs-badge">VS</div></div>
        <div class="score-side">
            <div class="score-agent green">Greedy Agent</div>
            <div class="score-val green" id="score2">—</div>
            <div class="score-meta" id="meta2">awaiting</div>
        </div>
    </div>

    <!-- Charts -->
    <div class="charts-grid" id="chartsArea" style="display:none">
        <div class="card">
            <div class="card-header">📈 Cumulative Reward Comparison</div>
            <canvas id="rewardChart" style="width:100%;height:220px;display:block"></canvas>
        </div>
        <div class="card">
            <div class="card-header">📊 Per-Step Reward</div>
            <canvas id="stepChart" style="width:100%;height:220px;display:block"></canvas>
        </div>
    </div>

    <!-- Arena: side-by-side logs -->
    <div class="arena">
        <div class="card">
            <div class="agent-header blue">
                <div class="agent-icon blue">🤖</div>
                <div><div class="agent-name">Fixed Strategy Agent</div><div class="agent-desc">Hardcoded optimal sequence per task</div></div>
            </div>
            <div class="log-panel" id="log1"><div class="log-empty">Awaiting start…</div></div>
        </div>
        <div class="card">
            <div class="agent-header green">
                <div class="agent-icon green">🧠</div>
                <div><div class="agent-name">Greedy Agent</div><div class="agent-desc">Priority-based heuristic decisions</div></div>
            </div>
            <div class="log-panel" id="log2"><div class="log-empty">Awaiting start…</div></div>
        </div>
    </div>

</div>

<script>
// Health check
async function checkHealth() {
    const d = document.getElementById('navDot'), t = document.getElementById('navStatus');
    try { const r = await fetch('/health'); if(r.ok){d.className='status-dot online';t.textContent='Online';t.style.color='#10b981';}else throw 0; }
    catch { d.className='status-dot';t.textContent='Offline';t.style.color='#ef4444'; }
}
checkHealth(); setInterval(checkHealth, 15000);

function renderLog(panelId, steps) {
    const p = document.getElementById(panelId);
    p.innerHTML = '';
    steps.forEach(s => {
        const cls = s.reward > 0 ? 'pos' : (s.reward < 0 ? 'neg' : 'neu');
        const rStr = (s.reward >= 0 ? '+' : '') + s.reward.toFixed(4);
        p.innerHTML += `<div class="log-entry">
            <div><div class="log-action">Step ${s.step}: ${s.action}</div><div class="log-desc">${(s.description||'').slice(0,80)}</div></div>
            <span class="log-reward ${cls}">${rStr}</span></div>`;
    });
}

function animateScore(id, target) {
    const el = document.getElementById(id);
    const t0 = performance.now();
    (function tick(now) {
        const p = Math.min((now - t0) / 800, 1);
        el.textContent = (target * (1 - Math.pow(1-p,3))).toFixed(4);
        if (p < 1) requestAnimationFrame(tick);
    })(performance.now());
}

// ── Chart drawing (matches dashboard style) ──
function drawLineChart(canvasId, labels, datasets) {
    const canvas = document.getElementById(canvasId);
    const W = canvas.parentElement.clientWidth - 48;
    const H = 220;
    canvas.width = W*2; canvas.height = H*2;
    canvas.style.width = W+'px'; canvas.style.height = H+'px';
    const ctx = canvas.getContext('2d');
    ctx.scale(2,2);
    ctx.clearRect(0,0,W,H);

    const allVals = datasets.flatMap(d => d.values);
    const maxV = Math.max(...allVals.map(Math.abs), 0.01);
    const minV = Math.min(...allVals, 0);
    const range = (maxV - minV) || 0.01;
    const pad = {l:48, r:12, t:14, b:32};
    const gW = W-pad.l-pad.r, gH = H-pad.t-pad.b;
    const n = labels.length;

    // Grid
    ctx.strokeStyle='#e5e7eb'; ctx.lineWidth=0.5;
    for(let i=0;i<=4;i++){
        const y=pad.t+gH*(1-i/4);
        ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(pad.l+gW,y);ctx.stroke();
        ctx.fillStyle='#9ca3af';ctx.font='9px Inter,sans-serif';ctx.textAlign='right';
        ctx.fillText((minV+range*i/4).toFixed(2),pad.l-5,y+3);
    }
    // X labels
    ctx.fillStyle='#9ca3af';ctx.font='9px Inter,sans-serif';ctx.textAlign='center';
    labels.forEach((l,i) => {
        if(n<=15 || i%Math.ceil(n/10)===0){
            const x=pad.l+(n===1?gW/2:(i/(n-1))*gW);
            ctx.fillText(l,x,pad.t+gH+18);
        }
    });

    // Draw each dataset
    datasets.forEach(ds => {
        // Gradient fill
        const grad=ctx.createLinearGradient(0,pad.t,0,pad.t+gH);
        grad.addColorStop(0,ds.color+'25');grad.addColorStop(1,ds.color+'05');
        ctx.beginPath();
        ds.values.forEach((v,i)=>{const x=pad.l+(n===1?gW/2:(i/(n-1))*gW),y=pad.t+gH*(1-(v-minV)/range);i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);});
        ctx.lineTo(pad.l+(n===1?gW/2:gW),pad.t+gH);ctx.lineTo(pad.l,pad.t+gH);ctx.closePath();
        ctx.fillStyle=grad;ctx.fill();

        // Line
        ctx.beginPath();ctx.lineWidth=2;ctx.strokeStyle=ds.color;ctx.lineJoin='round';
        ds.values.forEach((v,i)=>{const x=pad.l+(n===1?gW/2:(i/(n-1))*gW),y=pad.t+gH*(1-(v-minV)/range);i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);});
        ctx.stroke();

        // Dots
        ds.values.forEach((v,i)=>{
            const x=pad.l+(n===1?gW/2:(i/(n-1))*gW),y=pad.t+gH*(1-(v-minV)/range);
            ctx.beginPath();ctx.arc(x,y,i===n-1?4:2.5,0,Math.PI*2);ctx.fillStyle=ds.color;ctx.fill();
        });

        // Legend
        ctx.fillStyle=ds.color;ctx.font='bold 9px Inter,sans-serif';ctx.textAlign='left';
    });
    // Legend at top
    let lx = pad.l+4;
    datasets.forEach(ds=>{
        ctx.fillStyle=ds.color;ctx.font='bold 9px Inter,sans-serif';ctx.textAlign='left';
        ctx.fillText('● '+ds.label,lx,pad.t-3); lx+=ctx.measureText('● '+ds.label).width+14;
    });
}

function drawBarChart(canvasId, labels, datasets) {
    const canvas = document.getElementById(canvasId);
    const W = canvas.parentElement.clientWidth - 48;
    const H = 220;
    canvas.width = W*2; canvas.height = H*2;
    canvas.style.width = W+'px'; canvas.style.height = H+'px';
    const ctx = canvas.getContext('2d');
    ctx.scale(2,2);
    ctx.clearRect(0,0,W,H);

    const allVals = datasets.flatMap(d=>d.values);
    const maxV = Math.max(...allVals.map(Math.abs),0.01);
    const minV = Math.min(...allVals,0);
    const range = (maxV-minV)||0.01;
    const pad={l:48,r:12,t:14,b:32};
    const gW=W-pad.l-pad.r, gH=H-pad.t-pad.b;
    const n=labels.length;
    const groupW=gW/n;
    const barW=Math.min(groupW*0.35,18);

    // Grid
    ctx.strokeStyle='#e5e7eb';ctx.lineWidth=0.5;
    for(let i=0;i<=4;i++){const y=pad.t+gH*(1-i/4);ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(pad.l+gW,y);ctx.stroke();ctx.fillStyle='#9ca3af';ctx.font='9px Inter,sans-serif';ctx.textAlign='right';ctx.fillText((minV+range*i/4).toFixed(3),pad.l-5,y+3);}
    // X labels
    ctx.fillStyle='#9ca3af';ctx.font='9px Inter,sans-serif';ctx.textAlign='center';
    labels.forEach((l,i)=>{if(n<=15||i%Math.ceil(n/10)===0){const x=pad.l+groupW*(i+0.5);ctx.fillText(l,x,pad.t+gH+18);}});

    // Zero line
    const zeroY = pad.t+gH*(1-(0-minV)/range);
    ctx.strokeStyle='#d1d5db';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(pad.l,zeroY);ctx.lineTo(pad.l+gW,zeroY);ctx.stroke();

    // Bars
    datasets.forEach((ds,di)=>{
        ds.values.forEach((v,i)=>{
            const cx=pad.l+groupW*(i+0.5);
            const x=cx+(di-0.5)*barW-barW*0.1;
            const barH=Math.abs(v-0)/range*gH;
            const y=v>=0?zeroY-barH:zeroY;
            ctx.fillStyle=ds.color+'cc';
            ctx.beginPath();
            const r=2;
            ctx.moveTo(x+r,y);ctx.lineTo(x+barW-r,y);ctx.quadraticCurveTo(x+barW,y,x+barW,y+r);ctx.lineTo(x+barW,y+barH);ctx.lineTo(x,y+barH);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.fill();
        });
    });
    // Legend
    let lx=pad.l+4;
    datasets.forEach(ds=>{ctx.fillStyle=ds.color;ctx.font='bold 9px Inter,sans-serif';ctx.textAlign='left';ctx.fillText('● '+ds.label,lx,pad.t-3);lx+=ctx.measureText('● '+ds.label).width+14;});
}

async function startBattle() {
    const task = document.getElementById('taskSelect').value;
    const btn = document.getElementById('runBtn');
    const prog = document.getElementById('progText');
    const banner = document.getElementById('winnerBanner');

    btn.disabled = true; btn.textContent = '⏳ Running...';
    banner.className = 'winner-banner'; banner.style.display = 'none';
    document.getElementById('log1').innerHTML = '<div class="log-empty">⚙️ Running…</div>';
    document.getElementById('log2').innerHTML = '<div class="log-empty">⚙️ Running…</div>';
    document.getElementById('score1').textContent = '…';
    document.getElementById('score2').textContent = '…';
    document.getElementById('meta1').textContent = '';
    document.getElementById('meta2').textContent = '';
    document.getElementById('chartsArea').style.display = 'none';
    prog.textContent = 'Executing agents on ' + task.replace('task_','') + '…';

    try {
        const res = await fetch(`/api/compete-run?task_id=${encodeURIComponent(task)}&seed=42`);
        const data = await res.json();
        if (data.status !== 'ok') { alert('Error: ' + (data.message || JSON.stringify(data))); return; }

        // Render logs
        renderLog('log1', data.agent1.steps);
        renderLog('log2', data.agent2.steps);

        // Animate scores
        setTimeout(() => {
            animateScore('score1', data.agent1.final_score);
            animateScore('score2', data.agent2.final_score);
            document.getElementById('meta1').textContent = data.agent1.steps.length + ' steps';
            document.getElementById('meta2').textContent = data.agent2.steps.length + ' steps';
        }, 200);

        // Winner
        setTimeout(() => {
            const s1 = data.agent1.final_score.toFixed(4), s2 = data.agent2.final_score.toFixed(4);
            if (data.winner === 'agent1') {
                banner.className = 'winner-banner show blue-win';
                banner.innerHTML = `🏆 <strong>Fixed Strategy Wins!</strong> — Score ${s1} vs ${s2}`;
            } else if (data.winner === 'agent2') {
                banner.className = 'winner-banner show green-win';
                banner.innerHTML = `🏆 <strong>Greedy Agent Wins!</strong> — Score ${s2} vs ${s1}`;
            } else {
                banner.className = 'winner-banner show tie-win';
                banner.innerHTML = `🤝 <strong>It's a Tie!</strong> — Both scored ${s1}`;
            }
        }, 800);

        // Draw charts
        setTimeout(() => {
            document.getElementById('chartsArea').style.display = 'grid';
            const maxLen = Math.max(data.agent1.steps.length, data.agent2.steps.length);
            const labels = Array.from({length:maxLen}, (_,i) => 'S'+(i+1));
            const cum1 = data.agent1.steps.map(s => s.cumulative);
            const cum2 = data.agent2.steps.map(s => s.cumulative);
            // Pad shorter array
            while(cum1.length < maxLen) cum1.push(cum1[cum1.length-1]||0);
            while(cum2.length < maxLen) cum2.push(cum2[cum2.length-1]||0);

            requestAnimationFrame(() => {
                drawLineChart('rewardChart', labels, [
                    {label:'Fixed Strategy', values:cum1, color:'#2563eb'},
                    {label:'Greedy Agent', values:cum2, color:'#059669'},
                ]);
                const rew1 = data.agent1.steps.map(s => s.reward);
                const rew2 = data.agent2.steps.map(s => s.reward);
                while(rew1.length < maxLen) rew1.push(0);
                while(rew2.length < maxLen) rew2.push(0);
                drawBarChart('stepChart', labels, [
                    {label:'Fixed Strategy', values:rew1, color:'#2563eb'},
                    {label:'Greedy Agent', values:rew2, color:'#059669'},
                ]);
            });
        }, 500);

        prog.textContent = 'Battle complete!';
    } catch (err) {
        prog.textContent = 'Error: ' + err.message;
    } finally {
        btn.disabled = false; btn.textContent = '▶ Start Battle';
    }
}
</script>
</body>
</html>"""
