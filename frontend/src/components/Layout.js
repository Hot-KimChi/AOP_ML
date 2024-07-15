import { useState } from 'react';
import Head from 'next/head';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

export default function Layout({ children }) {
  const [sidebarActive, setSidebarActive] = useState(false);

  return (
    <>
      <Head>
        <title>AOP Database</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      
      <Navbar toggleSidebar={() => setSidebarActive(!sidebarActive)} />
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