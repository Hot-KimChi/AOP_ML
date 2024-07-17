import Layout from '@/components/Layout';
import { useState } from 'react';

export default function MeassetGeneration() {
  const [file, setFile] = useState(null);
  const [processedData, setProcessedData] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:5000/api/process-file', { // 백엔드 서버 주소로 변경
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          setProcessedData(data);
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
