import Link from 'next/link';

export default function Navbar({ toggleSidebar }) {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div className="container-fluid">
        <button className="btn btn-dark sidebar-toggle me-2" onClick={toggleSidebar}>
          <i className="fas fa-bars"></i>
        </button>
        <Link href="/" className="navbar-brand">
          AOP Database
        </Link>
        <div className="navbar-nav ms-auto">
          <select id="databaseSelect" className="form-select form-select-sm">
            <option value="">Select Database</option>
          </select>
        </div>
      </div>
    </nav>
  );
}
