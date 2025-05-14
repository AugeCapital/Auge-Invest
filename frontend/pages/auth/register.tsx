import { useState, FormEvent } from 'react';
import axios from 'axios';
import Head from 'next/head';
import Link from 'next/link';

// TODO: Move API base URL to an environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001'; // Assuming auth service runs on 8001

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    if (password !== confirmPassword) {
      setError('As senhas não coincidem.');
      setLoading(false);
      return;
    }
    if (password.length < 8) {
      setError('A senha deve ter pelo menos 8 caracteres.');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post(`${API_URL}/auth/register`, {
        email,
        password,
        full_name: fullName,
      });

      if (response.status === 201 && response.data) {
        setSuccess('Cadastro realizado com sucesso! Você já pode fazer o login.');
        console.log('Registration successful:', response.data);
        // Clear form
        setEmail('');
        setPassword('');
        setConfirmPassword('');
        setFullName('');
        // TODO: Optionally redirect to login page or show a success message with a link to login
      } else {
        setError('Falha no cadastro. Resposta inesperada do servidor.');
      }
    } catch (err: any) {
      if (axios.isAxiosError(err) && err.response) {
        if (err.response.data.detail) {
            if (err.response.data.detail === "Email already registered") {
                setError('Este email já está cadastrado.');
            } else {
                setError(err.response.data.detail);
            }
        } else {
            setError('Ocorreu um erro no cadastro.');
        }
      } else {
        setError('Ocorreu um erro de rede ou servidor. Tente novamente.');
      }
      console.error('Registration error:', err);
    }
    setLoading(false);
  };

  return (
    <>
      <Head>
        <title>Cadastro - Auge Invest</title>
      </Head>
      <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-auge-dark-bg py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8 bg-white dark:bg-auge-dark-card p-10 rounded-xl shadow-lg">
          <div>
            {/* TODO: Add Auge Invest Logo here */}
            <h2 className="mt-6 text-center text-3xl font-extrabold text-auge-light-text dark:text-auge-dark-text">
              Crie sua conta na Auge Invest
            </h2>
          </div>
          <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
            <div className="rounded-md shadow-sm -space-y-px">
              <div>
                <label htmlFor="full-name" className="sr-only">
                  Nome Completo
                </label>
                <input
                  id="full-name"
                  name="fullName"
                  type="text"
                  autoComplete="name"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 rounded-t-md focus:outline-none focus:ring-auge-blue focus:border-auge-blue dark:focus:ring-auge-green dark:focus:border-auge-green focus:z-10 sm:text-sm"
                  placeholder="Nome Completo"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                />
              </div>
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
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-auge-blue focus:border-auge-blue dark:focus:ring-auge-green dark:focus:border-auge-green focus:z-10 sm:text-sm"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
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
                  autoComplete="new-password"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-auge-blue focus:border-auge-blue dark:focus:ring-auge-green dark:focus:border-auge-green focus:z-10 sm:text-sm"
                  placeholder="Senha (mínimo 8 caracteres)"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <div>
                <label htmlFor="confirm-password" className="sr-only">
                  Confirmar Senha
                </label>
                <input
                  id="confirm-password"
                  name="confirmPassword"
                  type="password"
                  autoComplete="new-password"
                  required
                  className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white bg-white dark:bg-gray-700 rounded-b-md focus:outline-none focus:ring-auge-blue focus:border-auge-blue dark:focus:ring-auge-green dark:focus:border-auge-green focus:z-10 sm:text-sm"
                  placeholder="Confirmar Senha"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
            </div>

            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                <span className="block sm:inline">{error}</span>
              </div>
            )}
            {success && (
              <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
                <span className="block sm:inline">{success}</span>
              </div>
            )}

            <div>
              <button
                type="submit"
                disabled={loading}
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-auge-blue hover:bg-opacity-90 dark:bg-auge-green dark:hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-auge-blue dark:focus:ring-auge-green disabled:opacity-50"
              >
                {loading ? 'Cadastrando...' : 'Cadastrar'}
              </button>
            </div>
          </form>
          <div className="text-sm text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Já tem uma conta?
              <Link href="/auth/login" legacyBehavior>
                <a className="font-medium text-auge-blue hover:text-auge-blue-dark dark:text-auge-green dark:hover:text-auge-green-light ml-1">
                  Faça login
                </a>
              </Link>
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

