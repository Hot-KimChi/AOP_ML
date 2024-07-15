import { IncomingForm } from 'formidable';
import fs from 'fs';
import { exec } from 'child_process';

export const config = {
  api: {
    bodyParser: false,
  },
};

const processFile = async (req, res) => {
  const form = new IncomingForm();
  
  form.parse(req, (err, fields, files) => {
    if (err) {
      return res.status(500).json({ error: 'Error parsing file' });
    }

    const filePath = files.file.filepath;
    const scriptPath = './backend/app.py';  // Python 스크립트의 경로 수정

    // Python 스크립트 실행
    exec(`python ${scriptPath} ${filePath}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error}`);
        return res.status(500).json({ error: 'Error processing file' });
      }

      res.status(200).json({ data: stdout });
    });
  });
};

export default processFile;
