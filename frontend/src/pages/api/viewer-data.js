// import sql from 'mssql/msnodesqlv8';

// console.log('Environment variables:', {
//   DB_SERVER: process.env.DB_SERVER,
//   DB_NAME: process.env.DB_NAME
// });

// const config = {
//   server: process.env.DB_SERVER,
//   database: process.env.DB_NAME,
//   driver: 'msnodesqlv8',
//   options: {
//     trustedConnection: true
//   }
// };

// export default async function handler(req, res) {
//   try {
//     console.log('Attempting to connect to database...');
//     await sql.connect(config);
//     console.log('Connected to database successfully');
    
//     console.log('Executing query...');
//     const result = await sql.query`SELECT TOP 10 * FROM meas_setting`;
//     console.log('Query executed successfully');
    
//     res.status(200).json(result.recordset);
//   } catch (err) {
//     console.error('Error in API route:', err);
//     res.status(500).json({ error: err.message, stack: err.stack });
//   } finally {
//     await sql.close();
//   }
// }
import sql from 'mssql/msnodesqlv8';

const config = {
  server: process.env.DB_SERVER,
  database: process.env.DB_NAME,
  driver: 'msnodesqlv8',
  options: {
    trustedConnection: true
  }
};

export default async function handler(req, res) {
  const { tableName } = req.query;
  
  if (!tableName) {
    return res.status(400).json({ error: 'Table name is required' });
  }

  try {
    await sql.connect(config);
    
    // 테이블 이름의 유효성을 검사합니다
    const tableCheckResult = await sql.query`
      SELECT TABLE_NAME
      FROM INFORMATION_SCHEMA.TABLES
      WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME = ${tableName}
    `;
    
    if (tableCheckResult.recordset.length === 0) {
      return res.status(400).json({ error: 'Invalid table name' });
    }

    // 동적 SQL을 안전하게 구성합니다
    const query = `SELECT TOP 100 * FROM [${tableName}]`;
    const result = await sql.query(query);
    
    res.status(200).json(result.recordset);
  } catch (err) {
    console.error('Error in API route:', err);
    res.status(500).json({ error: err.message });
  } finally {
    await sql.close();
  }
}