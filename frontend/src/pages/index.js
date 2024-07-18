import Layout from '@/components/Layout';
import { useState, useEffect } from 'react';

export default function Home() {
  const [databases, setDatabases] = useState([]);
  const [selectedDatabase, setSelectedDatabase] = useState('');
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    authenticateUser();
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      fetchDatabases();
    }
  }, [isAuthenticated]);

  const authenticateUser = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/authenticate', {
        method: 'POST',
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
        setIsAuthenticated(data.authenticated);
      } else {
        const errorData = await response.json();
        setError(errorData.message);
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('인증 오류:', error);
      setError('인증 중 오류가 발생했습니다.');
      setIsAuthenticated(false);
    }
  };

  const fetchDatabases = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/get_databases', {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setDatabases(data.data);
        if (data.data.length > 0) {
          setSelectedDatabase(data.data[0]);
        }
      } else {
        console.error('데이터베이스 가져오기 실패');
      }
    } catch (error) {
      console.error('오류:', error);
    }
  };

  return (
    <Layout>
      <h1>AOP 데이터베이스에 오신 것을 환영합니다</h1>
      {isAuthenticated ? (
        <>
          {user && <p>로그인: {user}</p>}
          <div>
            <label htmlFor="database-select">데이터베이스 선택: </label>
            <select 
              id="database-select"
              value={selectedDatabase}
              onChange={(e) => setSelectedDatabase(e.target.value)}
            >
              {databases.map((db, index) => (
                <option key={index} value={db}>{db}</option>
              ))}
            </select>
          </div>
          <p>사이드바에서 옵션을 선택해주세요.</p>
        </>
      ) : (
        <p>{error || '인증에 실패했습니다. 관리자에게 문의하세요.'}</p>
      )}
    </Layout>
  );
}
