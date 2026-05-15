import "./globals.css"
export const metadata = { title: "Kutuliza - AI Medical Triage" }
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{margin:0}}>{children}</body>
    </html>
  )
}
