import { useState } from 'react';
import { DatabaseContext } from '@/contexts/DatabaseContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import '@/styles/globals.css';

function MyApp({ Component, pageProps }) {
  const [selectedDatabase, setSelectedDatabase] = useState('');

  return (
    <DatabaseContext.Provider value={{ selectedDatabase, setSelectedDatabase }}>
      <Component {...pageProps} />
    </DatabaseContext.Provider>
  );
}

export default MyApp;