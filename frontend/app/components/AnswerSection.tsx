'use client'

interface Citation {
  number: number
  source: string
  section: string
  title: string
  position: number
  excerpt?: string
}

interface Metrics {
  latency_ms: number
  token_estimate: number
  retrieved_chunks: number
}

interface AnswerResult {
  answer: string
  citations: Citation[]
  sources?: any[]
  metrics?: Metrics
  error?: string
}

export default function AnswerSection({ result }: { result: AnswerResult }) {
  if (result.error) {
    return (
      <div className="section">
        <h2>Error</h2>
        <div className="error">{result.error}</div>
      </div>
    )
  }

  const renderAnswerWithCitations = (answer: string) => {
    return answer.split(/(\[\d+\])/g).map((part, idx) =>
      /\[\d+\]/.test(part) ? (
        <sup key={idx} className="citation-ref">{part}</sup>
      ) : (
        <span key={idx}>{part}</span>
      )
    )
  }

  const metrics = result.metrics

  return (
    <div className="section">
      <h2>Answer</h2>

      <div className="answer-panel">
        {renderAnswerWithCitations(result.answer)}
      </div>

      {/* METRICS */}
      <div className="metrics">
        <div className="metric">
          <span className="metric-label">Response Time</span>
          <span>{metrics ? `${metrics.latency_ms.toFixed(1)} ms` : '—'}</span>
        </div>

        <div className="metric">
          <span className="metric-label">Token Estimate</span>
          <span>{metrics ? metrics.token_estimate : '—'}</span>
        </div>

        <div className="metric">
          <span className="metric-label">Retrieved Chunks</span>
          <span>{metrics ? metrics.retrieved_chunks : '—'}</span>
        </div>
      </div>

      {/* CITATIONS */}
     {/* CITATIONS */}
      {result.citations?.length > 0 && (
        <div className="citations-panel">
          <h3>Citations</h3>
          <ul className="sources-list">
            {result.citations.map((c) => (
              <li key={c.number}>
                <strong>[{c.number}]</strong>
                <div style={{ marginTop: '0.25rem' }}>
                  {c.excerpt ?? 'Referenced content'}
                </div>
                <div style={{ fontSize: '0.8rem', color: '#555' }}>
                  Source: {c.source} · Chunk {c.position + 1}
                </div>
            </li>
            
            ))}
          </ul>
        </div>
      )}


    </div>
  )
}
