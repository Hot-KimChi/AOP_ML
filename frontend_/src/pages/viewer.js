import React, { useState, useEffect, useMemo } from 'react';
import { useTable, useFilters, useSortBy } from 'react-table';
import { FaSort, FaSortUp, FaSortDown } from 'react-icons/fa';
import Layout from '../components/Layout';
import styles from '../styles/viewer.module.css';

// 기본 필터 UI 컴포넌트
function DefaultColumnFilter({
  column: { filterValue, setFilter, preFilteredRows }
}) {
  const count = preFilteredRows.length;

  return (
    <input
      value={filterValue || ''}
      onChange={e => {
        setFilter(e.target.value || undefined);
      }}
      placeholder={`Search ${count} records...`}
      className="form-control form-control-sm"
    />
  );
}

function ViewerTable({ columns, data }) {
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
    <div className={styles.tableContainer}>
      <table {...getTableProps()} className={`table table-striped ${styles.smallFontTable}`}>
        <thead>
          {headerGroups.map(headerGroup => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map(column => (
                <th {...column.getHeaderProps()}>
                  <div className={styles.header}>
                    <div className={styles.headerTextContainer}>
                      <span className={styles.headerText} title={column.render('Header')}>
                        {column.render('Header')}
                      </span>
                    </div>
                    <span {...column.getSortByToggleProps()} className={styles.headerIcon}>
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
                  <td {...cell.getCellProps()} title={String(cell.value)}>
                    {cell.render('Cell')}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
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

    if (selectedTable) {
      fetchData(selectedTable);
    }
  }, [selectedTable]);

  const columns = useMemo(() => {
    if (data.length === 0) return [];
    return Object.keys(data[0]).map(key => ({
      Header: key,
      accessor: key,
      Filter: DefaultColumnFilter,
    }));
  }, [data]);

  return (
    <Layout>
      <div className="d-flex align-items-center mb-3">
        <h2 className="me-3 mb-0">Viewer</h2>
        <select 
          value={selectedTable} 
          onChange={(e) => setSelectedTable(e.target.value)}
          className="form-select form-select-sm"
          style={{ width: '15%' }}
        >
          <option value="">Select a table</option>
          {tables.map((table) => (
            <option key={table} value={table}>{table}</option>
          ))}
        </select>
      </div>
      {loading && <p>Loading data...</p>}
      {error && <p>Error: {error}</p>}
      {!loading && !error && data.length === 0 && <p>No data available</p>}
      {!loading && !error && data.length > 0 && (
        <ViewerTable columns={columns} data={data} />
      )}
    </Layout>
  );
}

export default Viewer;
