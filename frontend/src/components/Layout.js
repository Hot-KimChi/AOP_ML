// import { useState } from 'react';
// import Head from 'next/head';
// import Navbar from './Navbar';
// import Sidebar from './Sidebar';

// export default function Layout({ children }) {
//   const [sidebarActive, setSidebarActive] = useState(false);

//   return (
//     <>
//       <Head>
//         <title>AOP Database</title>
//         <meta name="viewport" content="width=device-width, initial-scale=1" />
//       </Head>
      
//       <Navbar toggleSidebar={() => setSidebarActive(!sidebarActive)} />
//       <div className="container-fluid">
//         <div className="row">
          
//           <Sidebar active={sidebarActive} />
//           <main className={`col-md-9 ms-sm-auto col-lg-10 px-md-4 main-content ${sidebarActive ? 'active' : ''}`}>
//             {children}
//           </main>
        
//         </div>
//       </div>
//     </>
//   );
// }


import Navbar from './Navbar';
import Sidebar from './Sidebar';
import { useState } from 'react';

export default function Layout({ children, databases, selectedDatabase, setSelectedDatabase }) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="d-flex">
      <Navbar 
        toggleSidebar={toggleSidebar} 
        databases={databases}
        selectedDatabase={selectedDatabase}
        onDatabaseChange={setSelectedDatabase}
      />
      <Sidebar isOpen={isSidebarOpen} />
      <main className={`flex-grow-1 ${isSidebarOpen ? 'ms-240' : ''}`}>
        <div className="container-fluid mt-5 pt-3">
          {children}
        </div>
      </main>
    </div>
  );
}
