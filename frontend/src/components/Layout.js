import { useState, useEffect } from 'react';
import Head from 'next/head';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

export default function Layout({ children }) {
  const [sidebarActive, setSidebarActive] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [databases, setDatabases] = useState([]);
  const [selectedDatabase, setSelectedDatabase] = useState('');

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
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('인증 오류:', error);
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
    <>
      <Head>
        <title>AOP Database</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      
      <Navbar 
        toggleSidebar={() => setSidebarActive(!sidebarActive)} 
        isAuthenticated={isAuthenticated}
        user={user}
        databases={databases}
        selectedDatabase={selectedDatabase}
        setSelectedDatabase={setSelectedDatabase}
      />
      <div className="container-fluid">
        <div className="row">
          <Sidebar active={sidebarActive} />
          <main className={`col-md-9 ms-sm-auto col-lg-10 px-md-4 main-content ${sidebarActive ? 'active' : ''}`}>
            {children}
          </main>
        </div>
      </div>
    </>
  );
}
