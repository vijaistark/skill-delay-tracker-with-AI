import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        const data = await api.getDashboard();
        setDashboard(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchDashboard();
  }, []);

  if (loading) return <div className="empty-state">Loading...</div>;

  const user = JSON.parse(localStorage.getItem('user') || '{}');

  return (
    <div className="page-stack">
      <section className="panel">
        <p className="eyebrow">Skill Decay Tracker</p>
        <h1>Welcome back, {user.username || 'Learner'}.</h1>
      </section>

      <section className="stats-grid">
        <div className="stat-card">
          <span className="label">Learning Streak</span>
          <strong>🔥 {dashboard?.streak_days || 0} days</strong>
          <small>Keep learning today to continue your streak.</small>
        </div>

        <div className="stat-card">
          <span className="label">Total Learning</span>
          <strong>{Math.floor((dashboard?.total_minutes || 0) / 60)}h {((dashboard?.total_minutes || 0) % 60)}m</strong>
          <small>Across all tracked skills.</small>
        </div>
      </section>

      <section className="panel">
        <div className="section-head">
          <h2>Your Skills</h2>
          <Link to="/skills" className="secondary-button">View all</Link>
        </div>

        {dashboard?.skills?.length ? (
          <div className="skill-list compact">
            {dashboard.skills.map((skill) => (
              <div key={skill.id} className="skill-row">
                <div>
                  <strong>{skill.name}</strong>
                  <div className="meta-row">
                    <span>{skill.current_level}</span>
                    <span className="badge">{skill.decay_status || 'Healthy'}</span>
                    <span className="badge secondary">🔥 {skill.streak || 0} day streak</span>
                  </div>
                </div>
                <Link to={`/skills/${skill.id}`} className="tiny-button">View</Link>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">You haven’t added any skills yet.</div>
        )}
      </section>
    </div>
  );
}
