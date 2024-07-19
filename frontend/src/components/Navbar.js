import Link from 'next/link';
import { useState } from 'react';

export default function Navbar({ toggleSidebar, isAuthenticated, user, databases, selectedDatabase, setSelectedDatabase }) {
  const [error, setError] = useState(null);

  const handleLogin = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/authenticate', {
        method: 'POST',
        credentials: 'include'
      });
      if (response.ok) {
        window.location.reload();
      } else {
        const errorData = await response.json();
        setError(errorData.message);
      }
    } catch (error) {
      console.error('로그인 오류:', error);
      setError('로그인 중 오류가 발생했습니다.');
    }
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div className="container-fluid">
        <button className="btn btn-dark sidebar-toggle me-2" onClick={toggleSidebar}>
          <i className="fas fa-bars"></i>
        </button>
        <Link href="/" className="navbar-brand">
          AOP Database
        </Link>
        <div className="d-flex align-items-center ms-auto">
          {isAuthenticated ? (
            <>
              <span className="text-light me-2" style={{ whiteSpace: 'nowrap' }}>Welcome, {user}</span>
              <select 
                id="databaseSelect" 
                className="form-select form-select-sm"
                value={selectedDatabase}
                onChange={(e) => setSelectedDatabase(e.target.value)}
                style={{ height: '30px', fontSize: '0.875rem', width: 'auto' }}
              >
                <option value="">Select Database</option>
                {databases.map((db, index) => (
                  <option key={index} value={db}>{db}</option>
                ))}
              </select>
            </>
          ) : (
            <button className="btn btn-outline-light btn-sm" onClick={handleLogin}>Login</button>
          )}
        </div>
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
    </nav>
  );
}