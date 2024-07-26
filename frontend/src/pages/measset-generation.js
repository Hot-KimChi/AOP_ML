// import Layout from '@/components/Layout';
// import { useState } from 'react';

// export default function MeassetGeneration() {
//   const [file, setFile] = useState(null);
//   const [processedData, setProcessedData] = useState(null);

//   const handleFileChange = (event) => {
//     setFile(event.target.files[0]);
//   };

//   const handleFileUpload = async () => {
//     if (file) {
//       const formData = new FormData();
//       formData.append('file', file);

//       try {
//         const response = await fetch('http://localhost:5000/api/process-file', { // 백엔드 서버 주소로 변경
//           method: 'POST',
//           body: formData,
//         });

//         if (response.ok) {
//           const data = await response.json();
//           setProcessedData(data);
//         } else {
//           console.error('Failed to process the file');
//         }
//       } catch (error) {
//         console.error('Error:', error);
//       }
//     }
//   };

//   return (
//     <Layout>
//       <h2>MeasSet Generation</h2>
//       <input type="file" onChange={handleFileChange} />
//       <button onClick={handleFileUpload}>Upload and Process File</button>
//       {processedData && (
//         <div>
//           <h3>Processed Data:</h3>
//           <pre>{JSON.stringify(processedData, null, 2)}</pre>
//         </div>
//       )}
//     </Layout>
//   );
// }


import Layout from '@/components/Layout';
import { useState, useEffect } from 'react';

export default function MeassetGeneration() {
  const [file, setFile] = useState(null);
  const [database, setDatabase] = useState('');
  const [probes, setProbes] = useState([]);
  const [selectedProbe, setSelectedProbe] = useState('');
  const [processedData, setProcessedData] = useState(null);

  useEffect(() => {
    fetchProbes();
  }, []);

  const fetchProbes = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/get_probes', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setProbes(data.data);
      } else {
        console.error('Failed to fetch probes');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (file && selectedProbe) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('database', database);
      formData.append('probe', selectedProbe);

      try {
        const response = await fetch('http://localhost:5000/api/process-file', {
          method: 'POST',
          body: formData,
          credentials: 'include',
        });

        if (response.ok) {
          const data = await response.json();
          setProcessedData(data.data);
        } else {
          console.error('Failed to process the file');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  return (
    <Layout>
      <h2>MeasSet Generation</h2>
      <input type="file" onChange={handleFileChange} />
      <input
        type="text"
        placeholder="Database"
        value={database}
        onChange={(e) => setDatabase(e.target.value)}
      />
      <select
        value={selectedProbe}
        onChange={(e) => setSelectedProbe(e.target.value)}
      >
        <option value="">Select a probe</option>
        {probes.map((probe) => (
          <option key={probe.probeId} value={probe.probeId}>
            {probe.probeName} ({probe.probeId})
          </option>
        ))}
      </select>
      <button onClick={handleFileUpload}>Upload and Process File</button>
      {processedData && (
        <div>
          <h3>Processed Data:</h3>
          <pre>{JSON.stringify(processedData, null, 2)}</pre>
        </div>
      )}
    </Layout>
  );
}