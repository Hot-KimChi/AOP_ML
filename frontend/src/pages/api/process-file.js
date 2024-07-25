// import { IncomingForm } from 'formidable';
// import fs from 'fs';
// import { exec } from 'child_process';

// export const config = {
//   api: {
//     bodyParser: false,
//   },
// };

// const processFile = async (req, res) => {
//   const form = new IncomingForm();
  
//   form.parse(req, (err, fields, files) => {
//     if (err) {
//       return res.status(500).json({ error: 'Error parsing file' });
//     }

//     const filePath = files.file.filepath;
//     const scriptPath = './backend/backend_main.py';  // Python 스크립트의 경로 수정

//     // Python 스크립트 실행
//     exec(`python ${scriptPath} ${filePath}`, (error, stdout, stderr) => {
//       if (error) {
//         console.error(`Error executing Python script: ${error}`);
//         return res.status(500).json({ error: 'Error processing file' });
//       }

//       res.status(200).json({ data: stdout });
//     });
//   });
// };

// export default processFile;


import { IncomingForm } from 'formidable';

export const config = {
  api: {
    bodyParser: false,
  },
};

const processFile = async (req, res) => {
  const form = new IncomingForm();
  
  form.parse(req, async (err, fields, files) => {
    if (err) {
      return res.status(500).json({ error: 'Error parsing file' });
    }

    const filePath = files.file.filepath;

    try {
      // 백엔드 서버로 파일 경로 전송
      const backendResponse = await fetch('http://localhost:5000/process-file', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filePath }),
      });

      if (!backendResponse.ok) {
        throw new Error('Backend processing failed');
      }

      const data = await backendResponse.json();
      res.status(200).json(data);
    } catch (error) {
      console.error('Error processing file:', error);
      res.status(500).json({ error: 'Error processing file' });
    }
  });
};

export default processFile;