'use client'

import { useState } from 'react'

interface QuerySectionProps {
  onQuery: (query: string) => void
  isQuerying: boolean
}

export default function QuerySection({ onQuery, isQuerying }: QuerySectionProps) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      onQuery(query.trim())
    }
  }

  return (
    <div className="section">
      <h2>Query</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="query">Enter your question</label>
          <input
            type="text"
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="What would you like to know?"
            disabled={isQuerying}
          />
        </div>
        <button type="submit" className="button" disabled={isQuerying || !query.trim()}>
          {isQuerying ? 'Querying...' : 'Query'}
        </button>
      </form>
    </div>
  )
}
