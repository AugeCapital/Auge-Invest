import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Auge Invest",
  description: "Sua plataforma completa para o mercado financeiro brasileiro.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className={`${inter.className} bg-gray-100 dark:bg-auge-dark-bg text-auge-light-text dark:text-auge-dark-text`}>
        {/* TODO: Add a ThemeProvider for light/dark mode toggle if not handled by Tailwind darkMode class alone */}
        {/* TODO: Add a global Navbar and Footer component here */}
        <main className="min-h-screen">
          {children}
        </main>
      </body>
    </html>
  );
}

