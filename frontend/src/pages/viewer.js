// import { useState, useEffect } from 'react';
// import Layout from '../components/Layout';

// function Viewer() {
//   const [data, setData] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     async function fetchData() {
//       try {
//         console.log('Fetching data...');
//         const response = await fetch('/api/viewer-data');
//         console.log('Response status:', response.status);
//         if (!response.ok) {
//           throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const result = await response.json();
//         console.log('Fetched data:', result);
//         setData(result);
//       } catch (error) {
//         console.error("Fetching data failed:", error);
//         setError(error.message);
//       } finally {
//         setLoading(false);
//       }
//     }

//     fetchData();
//   }, []);

//   return (
//     <Layout>
//       <h2>Viewer</h2>
//       {loading ? (
//         <p>Loading data...</p>
//       ) : error ? (
//         <p>Error: {error}</p>
//       ) : data.length === 0 ? (
//         <p>No data available</p>
//       ) : (
//         <table className="table">
//           <thead>
//             <tr>
//               {Object.keys(data[0]).map((key) => (
//                 <th key={key}>{key}</th>
//               ))}
//             </tr>
//           </thead>
//           <tbody>
//             {data.map((item, index) => (
//               <tr key={index}>
//                 {Object.values(item).map((value, i) => (
//                   <td key={i}>{value}</td>
//                 ))}
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       )}
//     </Layout>
//   );
// }

// export default Viewer;

import { useState, useEffect } from 'react';
import Layout from '../components/Layout';

function Viewer() {
  const [tables, setTables] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchTables() {
      try {
        const response = await fetch('/api/tables');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        setTables(result);
      } catch (error) {
        console.error("Fetching tables failed:", error);
        setError(error.message);
      }
    }

    fetchTables();
  }, []);

  useEffect(() => {
    if (selectedTable) {
      fetchData(selectedTable);
    }
  }, [selectedTable]);

  async function fetchData(tableName) {
    setLoading(true);
    try {
      const response = await fetch(`/api/viewer-data?tableName=${tableName}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error("Fetching data failed:", error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout>
      <h2>Viewer</h2>
      <select 
        value={selectedTable} 
        onChange={(e) => setSelectedTable(e.target.value)}
        className="form-select mb-3"
      >
        <option value="">Select a table</option>
        {tables.map((table) => (
          <option key={table} value={table}>{table}</option>
        ))}
      </select>
      {loading ? (
        <p>Loading data...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : data.length === 0 ? (
        <p>No data available</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              {Object.keys(data[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                {Object.values(item).map((value, i) => (
                  <td key={i}>{value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Layout>
  );
}

export default Viewer;