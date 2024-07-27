import Link from 'next/link';
import { useState, useEffect, useContext } from 'react';
import { DatabaseContext } from '@/contexts/DatabaseContext';

export default function Navbar({ toggleSidebar, isAuthenticated, databases }) {
  const [error, setError] = useState(null);
  const [windowsUsername, setWindowsUsername] = useState('');
  const [fullName, setFullName] = useState('');
  const [connectionStatus, setConnectionStatus] = useState('');
  const { selectedDatabase, setSelectedDatabase } = useContext(DatabaseContext);

  useEffect(() => {
    if (isAuthenticated) {
      fetchWindowsUserInfo();
    }
  }, [isAuthenticated]);

  const fetchWindowsUserInfo = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/get_windows_user', {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setWindowsUsername(data.user);
        setFullName(data.full_name);
        setConnectionStatus(data.connection_status);
      } else {
        setConnectionStatus(data.connection_status);
        console.error('Windows 사용자 정보를 가져오는데 실패했습니다.');
      }
    } catch (error) {
      console.error('오류:', error);
      setConnectionStatus('연결 실패');
    }
  };

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
              <span className="text-light me-2" style={{ whiteSpace: 'nowrap' }}>{connectionStatus}, {fullName || windowsUsername}</span>
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