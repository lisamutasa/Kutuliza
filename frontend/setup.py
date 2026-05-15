import pathlib, os

# Create directories
dirs = ["src/app", "src/components", "src/hooks", "src/utils"]
for d in dirs:
    pathlib.Path(d).mkdir(parents=True, exist_ok=True)
    print(f"Created folder: {d}")

# globals.css
pathlib.Path("src/app/globals.css").write_text(
    "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n",
    encoding="utf-8"
)
print("Created globals.css")

# layout.jsx
pathlib.Path("src/app/layout.jsx").write_text(
    'import "./globals.css"\n'
    'export const metadata = { title: "Kutuliza - AI Medical Triage" }\n'
    'export default function RootLayout({ children }) {\n'
    '  return (\n'
    '    <html lang="en">\n'
    '      <body style={{margin:0}}>{children}</body>\n'
    '    </html>\n'
    '  )\n'
    '}\n',
    encoding="utf-8"
)
print("Created layout.jsx")

# page.jsx
pathlib.Path("src/app/page.jsx").write_text(
    '"use client"\n'
    'export default function Home() {\n'
    '  return (\n'
    '    <div style={{display:"flex",alignItems:"center",justifyContent:"center",\n'
    '      height:"100vh",background:"#f1f5f9",fontFamily:"sans-serif"}}>\n'
    '      <div style={{textAlign:"center"}}>\n'
    '        <h1 style={{fontSize:"2rem",fontWeight:"bold",color:"#0f172a"}}>\n'
    '          Kutuliza - AI Medical Triage\n'
    '        </h1>\n'
    '        <p style={{color:"#64748b",marginTop:"0.5rem"}}>\n'
    '          Backend connected. UI loading...\n'
    '        </p>\n'
    '      </div>\n'
    '    </div>\n'
    '  )\n'
    '}\n',
    encoding="utf-8"
)
print("Created page.jsx")

# tailwind.config.js
pathlib.Path("tailwind.config.js").write_text(
    'module.exports = {\n'
    '  content: ["./src/**/*.{js,ts,jsx,tsx}"],\n'
    '  theme: { extend: {} },\n'
    '  plugins: [],\n'
    '}\n',
    encoding="utf-8"
)
print("Created tailwind.config.js")

# postcss.config.js
pathlib.Path("postcss.config.js").write_text(
    'module.exports = {\n'
    '  plugins: { tailwindcss: {}, autoprefixer: {} },\n'
    '}\n',
    encoding="utf-8"
)
print("Created postcss.config.js")

# next.config.js
pathlib.Path("next.config.js").write_text(
    'module.exports = {}\n',
    encoding="utf-8"
)
print("Created next.config.js")

print("\nAll files created successfully!")