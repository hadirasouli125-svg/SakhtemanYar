import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = { title: 'ساختمان‌یار', description: 'مدیریت هوشمند ساختمان' }

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="fa" dir="rtl"><body>{children}</body></html>
}