import { useState, FormEvent, useEffect } from 'react';
import axios from 'axios';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useAuth } from '../../context/AuthContext'; // Adjusted path

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, user, isLoading: authLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Redirect if user is already logged in and not loading
    if (!authLoading && user) {
      router.push('/'); // Redirect to homepage or dashboard
    }
  }, [user, authLoading, router]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await axios.post(`${API_URL}/auth/login/access-token`, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      if (response.data.access_token) {
        await login(response.data.access_token); // Use AuthContext to login
        router.push('/'); // Redirect to homepage or dashboard after successful login
      } else {
        setError('Falha no login. Resposta inesperada do servidor.');
      }
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response) {
        if (err.response.status === 401) {
          setError('Email ou senha incorretos.');
        } else {
          setError(err.response.data.detail || 'Ocorreu um erro no login.');
        }
      } else {
        setError('Ocorreu um erro de rede ou servidor. Tente novamente.');
      }
      console.error('Login error:', err);
    }
    setLoading(false);
  };

  if (authLoading || (!authLoading && user)) {
    // Show loading indicator or null if user is already logged in (will be redirected)
    return <div className="min-h-screen flex items-center justify-center"><p>Carregando...</p></div>;
  }

  return (
    <>
      <Head>
        <title>Login - Auge Invest</title>
      </Head>
      <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-auge-dark-bg py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8 bg-white dark:bg-auge-dark-card p-10 rounded-xl shadow-lg">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-auge-light-text dark:text-auge-dark-text">
              Acesse sua conta
            </h2>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="email-address" className="sr-only">
                  Email
                </label>
                <input
                  id="email-address"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 rounded-t-md focus:outline-none focus:ring-auge-blue focus:border-auge-blue dark:focus:ring-auge-green dark:focus:border-auge-green focus:z-10 sm:text-sm"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                />
              </div>
              <div>
                <label htmlFor="password" className="sr-only">
                  Senha
                </label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 rounded-b-md focus:outline-none focus:ring-auge-blue focus:border-auge-blue dark:focus:ring-auge-green dark:focus:border-auge-green focus:z-10 sm:text-sm"
                  placeholder="Senha"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                <span className="block sm:inline">{error}</span>
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading || authLoading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-auge-blue hover:bg-opacity-90 dark:bg-auge-green dark:hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-auge-blue dark:focus:ring-auge-green disabled:opacity-50"
              >
                {loading ? 'Entrando...' : 'Entrar'}
              </button>
            </div>
          </form>
          <div className="text-sm text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Não tem uma conta?
              <a href="/auth/register" className="font-medium text-auge-blue hover:text-auge-blue-dark dark:text-auge-green dark:hover:text-auge-green-light ml-1">
                Cadastre-se
              </a>
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

