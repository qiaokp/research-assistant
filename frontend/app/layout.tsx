import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Research Assistant',
  description: 'AI-powered deep research assistant',
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
