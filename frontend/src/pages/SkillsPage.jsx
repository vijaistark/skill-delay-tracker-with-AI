import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';

export default function SkillsPage() {
  const [skills, setSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({
    name: '',
    category: '',
    current_level: 'Beginner',
    target_level: 'Intermediate',
    confidence: 5,
    daily_goal_minutes: 45,
  });

  const fetchSkills = async () => {
    try {
      const data = await api.getSkills();
      setSkills(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await api.createSkill(form);
      setForm({
        name: '',
        category: '',
        current_level: 'Beginner',
        target_level: 'Intermediate',
        confidence: 5,
        daily_goal_minutes: 45,
      });
      fetchSkills();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this skill?')) return;

    try {
      await api.deleteSkill(id);
      fetchSkills();
    } catch (err) {
      alert(err.message);
    }
  };

  if (loading) return <div className="empty-state">Loading...</div>;

  return (
    <div className="page-stack">
      <section className="panel">
        <div className="section-head">
          <h1>Your Skills</h1>
        </div>

        <form onSubmit={handleSubmit} className="skill-form">
          <input name="name" placeholder="Skill name" value={form.name} onChange={handleChange} />
          <input name="category" placeholder="Category" value={form.category} onChange={handleChange} />
          <select name="current_level" value={form.current_level} onChange={handleChange}>
            <option>Beginner</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>
          <select name="target_level" value={form.target_level} onChange={handleChange}>
            <option>Beginner</option>
            <option>Intermediate</option>
            <option>Advanced</option>
          </select>
          <input type="number" min="1" max="10" name="confidence" value={form.confidence} onChange={handleChange} />
          <input type="number" min="10" name="daily_goal_minutes" value={form.daily_goal_minutes} onChange={handleChange} />
          <button type="submit" className="primary-button">Add Skill</button>
        </form>
      </section>

      <section className="panel">
        {skills.length ? (
          <div className="skill-list">
            {skills.map((skill) => (
              <div key={skill.id} className="skill-card">
                <div className="skill-header">
                  <div>
                    <h3>{skill.name}</h3>
                    <p>{skill.category || 'General'}</p>
                  </div>
                  <span className="badge">{skill.current_level}</span>
                </div>

                <div className="meta-grid">
                  <div><span>Target</span><strong>{skill.target_level}</strong></div>
                  <div><span>Confidence</span><strong>{skill.confidence}/10</strong></div>
                  <div><span>Daily Goal</span><strong>{skill.daily_goal_minutes} min</strong></div>
                  <div><span>Last Practiced</span><strong>{skill.last_practiced || 'Not yet'}</strong></div>
                  <div><span>Decay Status</span><strong>{skill.decay_status || 'Healthy'}</strong></div>
                  <div><span>Progress</span><strong>{skill.progress_percent || 0}%</strong></div>
                </div>

                <div className="actions-row">
                  <Link to={`/skills/${skill.id}`} className="secondary-button">View</Link>
                  <button type="button" className="tiny-button" onClick={() => handleDelete(skill.id)}>Delete</button>
                </div>
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
