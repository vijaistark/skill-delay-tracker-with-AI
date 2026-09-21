import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function LearnPage() {
  const [skills, setSkills] = useState([]);
  const [form, setForm] = useState({
    skill: '',
    topic: '',
    duration_minutes: 30,
    confidence: 7,
    notes: '',
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    async function loadSkills() {
      try {
        const data = await api.getSkills();
        setSkills(data);
        if (data[0]) setForm((current) => ({ ...current, skill: data[0].id }));
      } catch (err) {
        console.error(err);
      }
    }

    loadSkills();
  }, []);

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      await api.createLearning({
        ...form,
        skill: Number(form.skill),
      });
      setMessage('Learning session completed. Your streak continues.');
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="page-stack">
      <section className="panel">
        <h1>Today's Learning</h1>

        <form onSubmit={handleSubmit} className="stack-form">
          <label>
            Select Skill
            <select name="skill" value={form.skill} onChange={handleChange}>
              {skills.map((skill) => (
                <option key={skill.id} value={skill.id}>{skill.name}</option>
              ))}
            </select>
          </label>

          <label>
            Topic
            <input name="topic" value={form.topic} onChange={handleChange} />
          </label>

          <label>
            Duration (minutes)
            <input type="number" min="1" name="duration_minutes" value={form.duration_minutes} onChange={handleChange} />
          </label>

          <label>
            Confidence (1-10)
            <input type="number" min="1" max="10" name="confidence" value={form.confidence} onChange={handleChange} />
          </label>

          <label>
            Notes
            <textarea name="notes" value={form.notes} onChange={handleChange} rows="4" />
          </label>

          <button type="submit" className="primary-button">Complete Learning Session</button>
          {message ? <div className="success-box">{message}</div> : null}
        </form>
      </section>
    </div>
  );
}
