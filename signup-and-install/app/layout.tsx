import { Inter } from 'next/font/google'
import { ClerkProvider } from '@clerk/nextjs'
import { Analytics } from '@vercel/analytics/react';


import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'YakBot',
  description: 'Chat your documents using monday.com and Slack',
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={inter.className}>
            {children}
            <Analytics />
        </body>
      </html>
    </ClerkProvider>
  )
}