import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function SkillDetailPage() {
  const { id } = useParams();
  const [skill, setSkill] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [skills, learning] = await Promise.all([api.getSkills(), api.getLearning()]);
      const selected = skills.find((item) => item.id === Number(id));
      setSkill(selected);
      setSessions(learning.filter((session) => session.skill === Number(id)));
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [id]);

  const generateSummary = async () => {
    try {
      const data = await api.getAiSummary({ skill_id: Number(id) });
      setSummary(data.summary);
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div className="empty-state">Loading...</div>;
  if (!skill) return <div className="empty-state">Skill not found.</div>;

  return (
    <div className="page-stack">
      <section className="panel">
        <div className="section-head">
          <h1>{skill.name}</h1>
          <Link to="/skills" className="secondary-button">Back to skills</Link>
        </div>

        <div className="meta-grid">
          <div><span>Category</span><strong>{skill.category || 'General'}</strong></div>
          <div><span>Current level</span><strong>{skill.current_level}</strong></div>
          <div><span>Target level</span><strong>{skill.target_level}</strong></div>
          <div><span>Confidence</span><strong>{skill.confidence}/10</strong></div>
          <div><span>Daily goal</span><strong>{skill.daily_goal_minutes} min</strong></div>
          <div><span>Last practiced</span><strong>{skill.last_practiced || 'Not yet'}</strong></div>
          <div><span>Decay status</span><strong>{skill.decay_status || 'Healthy'}</strong></div>
          <div><span>Progress</span><strong>{skill.progress_percent || 0}%</strong></div>
        </div>

        <div className="actions-row">
          <Link to="/learn" className="primary-button">Start Learning</Link>
          <button type="button" className="secondary-button" onClick={generateSummary}>Generate AI Summary</button>
        </div>
      </section>

      <section className="panel">
        <h2>Recent sessions</h2>
        {sessions.length ? (
          <div className="skill-list compact">
            {sessions.map((session) => (
              <div key={session.id} className="skill-row">
                <div>
                  <strong>{session.topic}</strong>
                  <div className="meta-row">
                    <span>{session.duration_minutes} min</span>
                    <span className="badge">{session.confidence}/10</span>
                  </div>
                </div>
                <small>{session.practiced_at}</small>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">Start your first learning session today.</div>
        )}
      </section>

      {summary ? (
        <section className="panel ai-box">
          <h2>AI Summary</h2>
          <p>{summary}</p>
        </section>
      ) : null}
    </div>
  );
}
