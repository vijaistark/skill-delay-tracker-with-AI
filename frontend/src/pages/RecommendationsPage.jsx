import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function RecommendationsPage() {
  const [data, setData] = useState({
    today_focus: '',
    reason: '',
    suggested_duration: 30,
    summary: '',
  });

  useEffect(() => {
    async function loadRecommendations() {
      try {
        const result = await api.getRecommendations();
        setData(result);
      } catch (err) {
        console.error(err);
      }
    }

    loadRecommendations();
  }, []);

  return (
    <div className="page-stack">
      <section className="panel">
        <h1>Today's Focus</h1>
        {data.today_focus ? (
          <>
            <h2>{data.today_focus}</h2>
            <p><strong>Reason:</strong> {data.reason}</p>
            <p><strong>Suggested duration:</strong> {data.suggested_duration} minutes</p>
          </>
        ) : (
          <p className="empty-state">Add a skill to start tracking recommendations.</p>
        )}
      </section>

      <section className="panel ai-box">
        <h2>AI Learning Summary</h2>
        <p>{data.summary || 'Start with a short daily practice session.'}</p>
      </section>
    </div>
  );
}
