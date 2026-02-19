import './globals.css';

export const metadata = {
  title: 'Pre-Delinquency Intervention Engine',
  description: 'AI-powered early warning system for customer financial stress prediction',
};

/**
 * Root layout component wrapping the entire dashboard.
 * Provides consistent header and page structure.
 */
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gray-50">
        {/* Top Navigation Bar */}
        <header className="bg-white border-b border-gray-200 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center gap-3">
                {/* Logo / Brand */}
                <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">PD</span>
                </div>
                <div>
                  <h1 className="text-lg font-bold text-gray-800">
                    Pre-Delinquency Engine
                  </h1>
                  <p className="text-xs text-gray-500 -mt-0.5">
                    Early Warning &amp; Intervention System
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                  * System Active
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {children}
        </main>
      </body>
    </html>
  );
}
