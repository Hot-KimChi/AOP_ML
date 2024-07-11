import React, { useState, useEffect, useMemo } from 'react';
import { useTable, useFilters, useSortBy } from 'react-table';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa';
import Layout from '../components/Layout';

// 기본 필터 UI 컴포넌트
function DefaultColumnFilter({
  column: { filterValue, preFilteredRows, setFilter },
}) {
  const count = preFilteredRows.length;

  return (
    <input
      value={filterValue || ''}
      onChange={e => {
        setFilter(e.target.value || undefined)
      }}
      placeholder={`Search ${count} records...`}
      className="form-control form-control-sm"
    />
  );
}

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
      } finally {
        setLoading(false);
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

  const columns = useMemo(() => {
    if (data.length === 0) return [];
    return Object.keys(data[0]).map(key => ({
      Header: key,
      accessor: key,
      Filter: DefaultColumnFilter,
    }));
  }, [data]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable(
    {
      columns,
      data,
    },
    useFilters,
    useSortBy
  );

  return (
    <Layout>
      <div className="d-flex align-items-center mb-3">
        <h2 className="me-3 mb-0">Viewer</h2>
        <select 
          value={selectedTable} 
          onChange={(e) => setSelectedTable(e.target.value)}
          className="form-select form-select-sm"
          style={{ width: '20%' }}
        >
          <option value="">Select a table</option>
          {tables.map((table) => (
            <option key={table} value={table}>{table}</option>
          ))}
        </select>
      </div>
      {loading ? (
        <p>Loading data...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : data.length === 0 ? (
        <p>No data available</p>
      ) : (
        <table {...getTableProps()} className="table table-striped table-bordered">
          <thead>
            {headerGroups.map(headerGroup => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map(column => (
                  <th {...column.getHeaderProps()}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span>{column.render('Header')}</span>
                      <span {...column.getSortByToggleProps()} style={{ cursor: 'pointer' }}>
                        {column.isSorted
                          ? column.isSortedDesc
                            ? <FaSortDown />
                            : <FaSortUp />
                          : <FaSort />}
                      </span>
                    </div>
                    <div>{column.canFilter ? column.render('Filter') : null}</div>
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody {...getTableBodyProps()}>
            {rows.map(row => {
              prepareRow(row);
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map(cell => (
                    <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </Layout>
  );
}

export default Viewer;



// import { useState, useEffect } from 'react';
// import Layout from '../components/Layout';

// function Viewer() {
//   const [tables, setTables] = useState([]);
//   const [selectedTable, setSelectedTable] = useState('');
//   const [data, setData] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     async function fetchTables() {
//       try {
//         const response = await fetch('/api/tables');
//         if (!response.ok) {
//           throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const result = await response.json();
//         setTables(result);
//       } catch (error) {
//         console.error("Fetching tables failed:", error);
//         setError(error.message);
//       }
//     }

//     fetchTables();
//   }, []);

//   useEffect(() => {
//     if (selectedTable) {
//       fetchData(selectedTable);
//     }
//   }, [selectedTable]);

//   async function fetchData(tableName) {
//     setLoading(true);
//     try {
//       const response = await fetch(`/api/viewer-data?tableName=${tableName}`);
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }
//       const result = await response.json();
//       setData(result);
//     } catch (error) {
//       console.error("Fetching data failed:", error);
//       setError(error.message);
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <Layout>
//       <h2>Viewer</h2>
//       <select 
//         value={selectedTable} 
//         onChange={(e) => setSelectedTable(e.target.value)}
//         className="form-select mb-3"
//       >
//         <option value="">Select a table</option>
//         {tables.map((table) => (
//           <option key={table} value={table}>{table}</option>
//         ))}
//       </select>
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



// import { useState, useEffect, useMemo } from 'react';
// import { useTable, useFilters, useSortBy } from 'react-table';
// import Layout from '../components/Layout';

// // 기본 필터 UI 컴포넌트
// function DefaultColumnFilter({
//   column: { filterValue, preFilteredRows, setFilter },
// }) {
//   const count = preFilteredRows.length;

//   return (
//     <input
//       value={filterValue || ''}
//       onChange={e => {
//         setFilter(e.target.value || undefined)
//       }}
//       placeholder={`Search ${count} records...`}
//       className="form-control form-control-sm"
//     />
//   );
// }

// function Viewer() {
//   const [tables, setTables] = useState([]);
//   const [selectedTable, setSelectedTable] = useState('');
//   const [data, setData] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     async function fetchTables() {
//       try {
//         const response = await fetch('/api/tables');
//         if (!response.ok) {
//           throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const result = await response.json();
//         setTables(result);
//       } catch (error) {
//         console.error("Fetching tables failed:", error);
//         setError(error.message);
//       } finally {
//         setLoading(false);
//       }
//     }

//     fetchTables();
//   }, []);

//   useEffect(() => {
//     if (selectedTable) {
//       fetchData(selectedTable);
//     }
//   }, [selectedTable]);

//   async function fetchData(tableName) {
//     setLoading(true);
//     try {
//       const response = await fetch(`/api/viewer-data?tableName=${tableName}`);
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }
//       const result = await response.json();
//       setData(result);
//     } catch (error) {
//       console.error("Fetching data failed:", error);
//       setError(error.message);
//     } finally {
//       setLoading(false);
//     }
//   }

//   const columns = useMemo(() => {
//     if (data.length === 0) return [];
//     return Object.keys(data[0]).map(key => ({
//       Header: key,
//       accessor: key,
//       Filter: DefaultColumnFilter,
//     }));
//   }, [data]);

//   const {
//     getTableProps,
//     getTableBodyProps,
//     headerGroups,
//     rows,
//     prepareRow,
//   } = useTable(
//     {
//       columns,
//       data,
//     },
//     useFilters,
//     useSortBy
//   );

//   return (
//     <Layout>
//       <div className="d-flex align-items-center mb-3">
//         <h2 className="me-3 mb-0">Viewer</h2>
//         <select 
//           value={selectedTable} 
//           onChange={(e) => setSelectedTable(e.target.value)}
//           className="form-select form-select-sm"
//           style={{ width: '20%' }}
//         >
//           <option value="">Select a table</option>
//           {tables.map((table) => (
//             <option key={table} value={table}>{table}</option>
//           ))}
//         </select>
//       </div>
//       {loading ? (
//         <p>Loading data...</p>
//       ) : error ? (
//         <p>Error: {error}</p>
//       ) : data.length === 0 ? (
//         <p>No data available</p>
//       ) : (
//         <table {...getTableProps()} className="table table-striped table-bordered">
//           <thead>
//             {headerGroups.map(headerGroup => (
//               <tr {...headerGroup.getHeaderGroupProps()}>
//                 {headerGroup.headers.map(column => (
//                   <th {...column.getHeaderProps(column.getSortByToggleProps())}>
//                     {column.render('Header')}
//                     <span>
//                       {column.isSorted
//                         ? column.isSortedDesc
//                           ? ' 🔽'
//                           : ' 🔼'
//                         : ''}
//                     </span>
//                     <div>{column.canFilter ? column.render('Filter') : null}</div>
//                   </th>
//                 ))}
//               </tr>
//             ))}
//           </thead>
//           <tbody {...getTableBodyProps()}>
//             {rows.map(row => {
//               prepareRow(row);
//               return (
//                 <tr {...row.getRowProps()}>
//                   {row.cells.map(cell => (
//                     <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
//                   ))}
//                 </tr>
//               );
//             })}
//           </tbody>
//         </table>
//       )}
//     </Layout>
//   );
// }

// export default Viewer;


// import React, { useState, useEffect, useMemo } from 'react';
// import { useTable, useFilters, useSortBy } from 'react-table';
// import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa';
// import Layout from '../components/Layout';

// // 기본 필터 UI 컴포넌트
// function DefaultColumnFilter({
//   column: { filterValue, preFilteredRows, setFilter },
// }) {
//   const count = preFilteredRows.length;

//   return (
//     <input
//       value={filterValue || ''}
//       onChange={e => {
//         setFilter(e.target.value || undefined)
//       }}
//       placeholder={`Search ${count} records...`}
//       className="form-control form-control-sm"
//     />
//   );
// }

// function Viewer() {
//   const [tables, setTables] = useState([]);
//   const [selectedTable, setSelectedTable] = useState('');
//   const [data, setData] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     async function fetchTables() {
//       try {
//         const response = await fetch('/api/tables');
//         if (!response.ok) {
//           throw new Error(`HTTP error! status: ${response.status}`);
//         }
//         const result = await response.json();
//         setTables(result);
//       } catch (error) {
//         console.error("Fetching tables failed:", error);
//         setError(error.message);
//       } finally {
//         setLoading(false);
//       }
//     }

//     fetchTables();
//   }, []);

//   useEffect(() => {
//     if (selectedTable) {
//       fetchData(selectedTable);
//     }
//   }, [selectedTable]);

//   async function fetchData(tableName) {
//     setLoading(true);
//     try {
//       const response = await fetch(`/api/viewer-data?tableName=${tableName}`);
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }
//       const result = await response.json();
//       setData(result);
//     } catch (error) {
//       console.error("Fetching data failed:", error);
//       setError(error.message);
//     } finally {
//       setLoading(false);
//     }
//   }

//   const columns = useMemo(() => {
//     if (data.length === 0) return [];
//     return Object.keys(data[0]).map(key => ({
//       Header: key,
//       accessor: key,
//       Filter: DefaultColumnFilter,
//     }));
//   }, [data]);

//   const {
//     getTableProps,
//     getTableBodyProps,
//     headerGroups,
//     rows,
//     prepareRow,
//   } = useTable(
//     {
//       columns,
//       data,
//     },
//     useFilters,
//     useSortBy
//   );

//   return (
//     <Layout>
//       <div className="d-flex align-items-center mb-3">
//         <h2 className="me-3 mb-0">Viewer</h2>
//         <select 
//           value={selectedTable} 
//           onChange={(e) => setSelectedTable(e.target.value)}
//           className="form-select form-select-sm"
//           style={{ width: '20%' }}
//         >
//           <option value="">Select a table</option>
//           {tables.map((table) => (
//             <option key={table} value={table}>{table}</option>
//           ))}
//         </select>
//       </div>
//       {loading ? (
//         <p>Loading data...</p>
//       ) : error ? (
//         <p>Error: {error}</p>
//       ) : data.length === 0 ? (
//         <p>No data available</p>
//       ) : (
//         <table {...getTableProps()} className="table table-striped table-bordered">
//           <thead>
//             {headerGroups.map(headerGroup => (
//               <tr {...headerGroup.getHeaderGroupProps()}>
//                 {headerGroup.headers.map(column => (
//                   <th {...column.getHeaderProps(column.getSortByToggleProps())}>
//                     <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
//                       <span>{column.render('Header')}</span>
//                       <span>
//                         {column.isSorted
//                           ? column.isSortedDesc
//                             ? <FaSortDown />
//                             : <FaSortUp />
//                           : <FaSort />}
//                       </span>
//                     </div>
//                     <div>{column.canFilter ? column.render('Filter') : null}</div>
//                   </th>
//                 ))}
//               </tr>
//             ))}
//           </thead>
//           <tbody {...getTableBodyProps()}>
//             {rows.map(row => {
//               prepareRow(row);
//               return (
//                 <tr {...row.getRowProps()}>
//                   {row.cells.map(cell => (
//                     <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
//                   ))}
//                 </tr>
//               );
//             })}
//           </tbody>
//         </table>
//       )}
//     </Layout>
//   );
// }

// export default Viewer;