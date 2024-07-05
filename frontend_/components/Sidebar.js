import styles from '../styles/Home.module.css'

export default function Sidebar({ setActiveContent }) {
  return (
    <nav className={styles.sidebar}>
      <ul>
        <li onClick={() => setActiveContent('meassetGeneration')}>MeasSet Generation</li>
        <li onClick={() => setActiveContent('viewer')}>Viewer</li>
        <li onClick={() => setActiveContent('verificationReport')}>Verification Report</li>
        <li onClick={() => setActiveContent('machineLearning')}>Machine Learning</li>
      </ul>
    </nav>
  )
}