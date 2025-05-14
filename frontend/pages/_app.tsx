import type { AppProps } from "next/app";
import { Inter } from "next/font/google";
import "../styles/globals.css"; // Adjusted path for styles folder
import { AuthProvider } from "../context/AuthContext"; // Import AuthProvider

const inter = Inter({ subsets: ["latin"] });

// export const metadata: Metadata = { // Metadata is usually defined per-page or in RootLayout for App Router
// title: "Auge Invest",
// description: "Sua plataforma completa para o mercado financeiro brasileiro.",
// };

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider> {/* Wrap the application with AuthProvider */}
      {/* It's common to have a RootLayout component here if using Next.js 13+ App Router, 
          but for Pages Router, this structure is fine. 
          The className for body is usually in a Layout component or _document.tsx for global body styles.
      */}
      {/* <div lang="pt-BR" className={`${inter.className} bg-gray-100 dark:bg-auge-dark-bg text-auge-light-text dark:text-auge-dark-text`}> */}
      {/* Consider moving global layout elements (like Navbar, Footer, and body styling) to a Layout component */}
      <main className={`${inter.className} min-h-screen bg-gray-100 dark:bg-auge-dark-bg text-auge-light-text dark:text-auge-dark-text`}>
        <Component {...pageProps} />
      </main>
      {/* </div> */}
    </AuthProvider>
  );
}

