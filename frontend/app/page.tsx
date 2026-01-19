'use client'

import { useState } from 'react'
import UploadSection from './components/UploadSection'
import QuerySection from './components/QuerySection'
import AnswerSection from './components/AnswerSection'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function Home() {
  const [queryResult, setQueryResult] = useState<any>(null)
  const [isQuerying, setIsQuerying] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<string | null>(null)

  const handleQuery = async (query: string) => {
    setIsQuerying(true)
    setQueryResult(null)
    
    try {
      const response = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ q: query }),
      })
      
      if (!response.ok) {
        throw new Error(`Query failed: ${response.statusText}`)
      }
      
      const data = await response.json()
      setQueryResult(data)
    } catch (error: any) {
      setQueryResult({ error: error.message })
    } finally {
      setIsQuerying(false)
    }
  }

  const handleUpload = async (text: string, file: File | null, source: string) => {
    setUploadStatus(null)
    
    try {
      const formData = new FormData()
      
      if (file) {
        formData.append('file', file)
      } else if (text) {
        formData.append('text', text)
      } else {
        throw new Error('Either text or file must be provided')
      }
      
      formData.append('source', source)
      formData.append('section', 'main')
      

      
      const response = await fetch(`${API_URL}/ingest`, {
        method: 'POST',
        body: formData,
      })
      
 
      if (!response.ok) {
        const errorText = await response.text()
       
        throw new Error(`Upload failed: ${response.statusText}`)
      }
      
      const data = await response.json()
    
      setUploadStatus(`Successfully ingested ${data.count} chunks into collection "${data.collection_name}"`)
    } catch (error: any) {
      setUploadStatus(`Error: ${error.message}`)
    }
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Mini RAG Application</h1>
        <p>Turn your documents into an intelligent knowledge base</p>
      </div>

      <UploadSection onUpload={handleUpload} status={uploadStatus} />

      <QuerySection onQuery={handleQuery} isQuerying={isQuerying} />

      {queryResult && (
        <AnswerSection result={queryResult} />
      )}
    </div>
  )
}
