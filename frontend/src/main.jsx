import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "http://localhost:8000";

function Card({title, value, unit=""}) {
  return <div className="card"><div className="label">{title}</div><div className="value">{value}<span>{unit}</span></div></div>;
}

function App() {
  const [system, setSystem] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [message, setMessage] = useState("");

  async function refresh() {
    const s = await fetch(`${API}/api/system`).then(r => r.json());
    setSystem(s);
    const j = await fetch(`${API}/api/jobs`).then(r => r.json());
    setJobs(j);
  }

  async function runJob(name) {
    setMessage("Running automation...");
    const result = await fetch(`${API}/api/jobs/${name}`, {method:"POST"}).then(r => r.json());
    setMessage(`${result.name}: ${result.status}`);
    refresh();
  }

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 5000);
    return () => clearInterval(id);
  }, []);

  if (!system) return <div className="loading">Loading server metrics...</div>;

  const uptime = Math.floor(system.uptime_seconds / 3600) + "h " +
                 Math.floor((system.uptime_seconds % 3600) / 60) + "m";

  return (
    <main>
      <header>
        <div>
          <div className="eyebrow">LINUXOPS</div>
          <h1>Server Monitoring & Automation</h1>
          <p>{system.hostname} · {system.os}</p>
        </div>
        <button onClick={refresh}>Refresh</button>
      </header>

      <section className="grid">
        <Card title="CPU" value={system.cpu_percent} unit="%" />
        <Card title="Memory" value={system.memory_percent} unit="%" />
        <Card title="Disk" value={system.disk_percent} unit="%" />
        <Card title="Processes" value={system.process_count} />
        <Card title="Uptime" value={uptime} />
        <Card title="Network" value={`${system.network_sent_mb} / ${system.network_recv_mb}`} unit=" MB" />
      </section>

      <section className="panel">
        <h2>Safe Automation Jobs</h2>
        <div className="buttons">
          <button onClick={() => runJob("health-check")}>Health Check</button>
          <button onClick={() => runJob("dependency-check")}>Dependency Check</button>
          <button onClick={() => runJob("disk-check")}>Disk Check</button>
        </div>
        {message && <div className="message">{message}</div>}
      </section>

      <section className="panel">
        <h2>Recent Automation</h2>
        {jobs.length === 0 ? <p>No jobs yet.</p> :
          <div className="table">
            {jobs.map(j => (
              <div className="row" key={j.id}>
                <span>{j.name}</span>
                <span className={j.status}>{j.status}</span>
                <code>{j.output}</code>
              </div>
            ))}
          </div>
        }
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
