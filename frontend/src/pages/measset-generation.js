import Layout from '@/components/Layout';
import { useState, useEffect, useContext } from 'react';
import { DatabaseContext } from '@/contexts/DatabaseContext';

export default function MeassetGeneration() {
  const [file, setFile] = useState(null);
  const { selectedDatabase } = useContext(DatabaseContext);
  const [probes, setProbes] = useState([]);
  const [selectedProbe, setSelectedProbe] = useState('');
  const [processedData, setProcessedData] = useState(null);

  useEffect(() => {
    if (selectedDatabase) {
      fetchProbes();
    }
  }, [selectedDatabase]);

  const fetchProbes = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/get_probes?database=${selectedDatabase}`, {
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
    if (file && selectedProbe && selectedDatabase) {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('database', selectedDatabase);
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

  // return (
  //   <Layout>
  //     <h2>MeasSet Generation</h2>
  //     <p>Selected Database: {selectedDatabase || 'None'}</p>
  //     <input type="file" onChange={handleFileChange} />
  //     <select
  //       value={selectedProbe}
  //       onChange={(e) => setSelectedProbe(e.target.value)}
  //     >
  //       <option value="">Select a probe</option>
  //       {probes.map((probe) => (
  //         <option key={probe.probeId} value={probe.probeIid}>
  //           {probe.probeName} ({probe.probeId})
  //         </option>
  //       ))}
  //     </select>
  //     <button onClick={handleFileUpload} disabled={!selectedDatabase}>Upload and Process File</button>
  //     {processedData && (
  //       <div>
  //         <h3>Processed Data:</h3>
  //         <pre>{JSON.stringify(processedData, null, 2)}</pre>
  //       </div>
  //     )}
  //   </Layout>
  // );

  return (
    <Layout>
      <div className="container mt-5">
        <h2 className="mb-4">MeasSet Generation</h2>
        <div className="alert alert-info">
          Selected Database: {selectedDatabase || 'None'}
        </div>
        <div className="card">
          <div className="card-body">
            <div className="mb-3">
              <label htmlFor="fileInput" className="form-label">Choose File</label>
              <input type="file" className="form-control" id="fileInput" onChange={handleFileChange} />
            </div>
            <div className="mb-3">
              <label htmlFor="probeSelect" className="form-label">Select Probe</label>
              <select
                id="probeSelect"
                className="form-select"
                value={selectedProbe}
                onChange={(e) => setSelectedProbe(e.target.value)}
              >
                <option value="">Select a probe</option>
                {probes.map((probe) => (
                  <option key={probe.probeId} value={probe.probeIid}>
                    {probe.probeName} ({probe.probeId})
                  </option>
                ))}
              </select>
            </div>
            <button 
              className="btn btn-primary" 
              onClick={handleFileUpload} 
              disabled={!selectedDatabase}
            >
              Upload and Process File
            </button>
          </div>
        </div>
        {processedData && (
          <div className="mt-4">
            <h3>Processed Data:</h3>
            <pre className="bg-light p-3 rounded">
              {JSON.stringify(processedData, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </Layout>
  );
}