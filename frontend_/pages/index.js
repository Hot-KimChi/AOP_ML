import { useState } from 'react'
import Layout from '../components/Layout'
import Sidebar from '../components/Sidebar'
import Content from '../components/Content'

export default function Home() {
  const [activeContent, setActiveContent] = useState('meassetGeneration')

  return (
    <Layout>
      <Sidebar setActiveContent={setActiveContent} />
      <Content activeContent={activeContent} />
    </Layout>
  )
}