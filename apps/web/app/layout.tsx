import './globals.css';
import { AppProvider } from '@/lib/store';
import { Sidebar } from '@/components/Sidebar';
import { Header } from '@/components/Header';
import { CommandPalette } from '@/components/CommandPalette';

export const metadata = {
  title: 'SentinelEdge — Explainable AI-Assisted Cyber Resilience',
  description: 'Research prototype for lightweight security monitoring, incident investigation, business-impact assessment, and recovery readiness.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-editorial-bg text-editorial-text flex antialiased">
        <AppProvider>
          <Sidebar />
          <div className="flex-1 flex flex-col min-w-0">
            <Header />
            <main className="flex-1 p-6 overflow-y-auto">
              {children}
            </main>
          </div>
          <CommandPalette />
        </AppProvider>
      </body>
    </html>
  );
}
