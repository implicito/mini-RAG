'use client'

import { useState } from 'react'
import * as React from 'react'

interface UploadSectionProps {
  onUpload: (text: string, file: File | null, source: string) => void
  status: string | null
}

export default function UploadSection({ onUpload, status }: UploadSectionProps) {
  const [text, setText] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [source, setSource] = useState('upload')
  const [isUploading, setIsUploading] = useState(false)
  
  // #region agent log
  React.useEffect(() => {
    const fileInput = document.getElementById('file') as HTMLInputElement
    if (fileInput) {
      fetch('https://mini-rag-4b08.onrender.com/ingest/b8f754dd-42c4-46cb-9f90-df7dbbea1fe9',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'UploadSection.tsx:18',message:'File input state check',data:{disabled:fileInput.disabled,textLength:text.length,hasFile:file!==null,display:window.getComputedStyle(fileInput).display,visibility:window.getComputedStyle(fileInput).visibility,pointerEvents:window.getComputedStyle(fileInput).pointerEvents},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'I'})}).catch(()=>{});
    }
  }, [text, file])
  // #endregion

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsUploading(true)
    
    try {
      await onUpload(text, file, source)
      // Reset form on success
      if (status && !status.startsWith('Error')) {
        setText('')
        setFile(null)
        setSource('upload')
      
      }
    } finally {
      setIsUploading(false)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // #region agent log
    fetch('https://mini-rag-4b08.onrender.com/ingest/b8f754dd-42c4-46cb-9f90-df7dbbea1fe9',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'UploadSection.tsx:35',message:'handleFileChange called',data:{hasFiles:e.target.files!==null,filesCount:e.target.files?.length||0},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'F'})}).catch(()=>{});
    // #endregion
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setText('') // Clear text when file is selected
    }
  }
  
  const handleFileInputClick = (e: React.MouseEvent<HTMLInputElement>) => {
    // #region agent log
    fetch('https://mini-rag-4b08.onrender.com/ingest/b8f754dd-42c4-46cb-9f90-df7dbbea1fe9',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'UploadSection.tsx:42',message:'File input clicked',data:{disabled:!!text},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'G'})}).catch(()=>{});
    // #endregion
  }
  
  const handleLabelClick = (e: React.MouseEvent<HTMLLabelElement>) => {
    // #region agent log
    fetch('https://mini-rag-4b08.onrender.com/ingest/b8f754dd-42c4-46cb-9f90-df7dbbea1fe9',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'UploadSection.tsx:48',message:'Label clicked',data:{textLength:text.length,hasFile:file!==null},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'H'})}).catch(()=>{});
    // #endregion
  }

  return (
    <div className="section">
      <h2>Upload Documents</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="source">Source Identifier</label>
          <input
            type="text"
            id="source"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="e.g., document-1, article-2024"
          />
        </div>

        <div className="input-group">
          <label htmlFor="text">Paste Text</label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => {
              setText(e.target.value)
              setFile(null) // Clear file when text is entered
            }}
            placeholder="Paste your document text here..."
            disabled={!!file}
          />
        </div>

        <div className="input-group">
          <label htmlFor="file" onClick={handleLabelClick}>Or Upload File</label>
          <input
            type="file"
            id="file"
            accept=".txt,.md,.pdf"
            onChange={handleFileChange}
            onClick={handleFileInputClick}
            disabled={!!text}
          />
        </div>

        <button type="submit" className="button" disabled={isUploading || (!text && !file)}>
          {isUploading ? 'Uploading...' : 'Upload & Ingest'}
        </button>
      </form>

      {status && (
        <div className={status.startsWith('Error') ? 'error' : 'success'}>
          {status}
        </div>
      )}
    </div>
  )
}
