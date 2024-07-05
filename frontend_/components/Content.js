import { useEffect, useState } from 'react'
import styles from '../styles/Home.module.css'

export default function Content({ activeContent }) {
  const [data, setData] = useState(null)

  useEffect(() => {
    if (activeContent === 'meassetGeneration') {
      fetch('/api/measset')
        .then(res => res.json())
        .then(data => setData(data))
    }
  }, [activeContent])

  return (
    <div className={styles.content}>
      {activeContent === 'meassetGeneration' && (
        <>
          <h2>MeasSet Generation</h2>
          {data && (
            <>
              <p>ID: {data.id}</p>
              <p>Name: {data.name}</p>
              <p>Description: {data.description}</p>
            </>
          )}
        </>
      )}
      {/* Add other content components here */}
    </div>
  )
}