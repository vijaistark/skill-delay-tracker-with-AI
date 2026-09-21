import { Link, NavLink, Outlet } from 'react-router-dom';

export default function Layout() {
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-wrap">
          <Link to="/dashboard" className="brand">Skill Decay Tracker</Link>
        </div>

        <nav className="nav" aria-label="Main navigation">
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/skills">Skills</NavLink>
          <NavLink to="/learn">Learn</NavLink>
          <NavLink to="/recommendations">Recommendations</NavLink>
          <button type="button" className="link-button" onClick={handleLogout}>Logout</button>
        </nav>
      </header>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
