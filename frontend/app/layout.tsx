import './globals.css'

export const metadata = {
  title: 'Mini RAG App',
  description: 'Retrieval-Augmented Generation Application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
