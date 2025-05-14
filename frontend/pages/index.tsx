import Head from 'next/head';

export default function HomePage() {
  return (
    <>
      <Head>
        <title>Auge Invest - Início</title>
        <meta name="description" content="Bem-vindo à Auge Invest, sua plataforma completa para o mercado financeiro brasileiro." />
      </Head>
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-auge-blue dark:text-white">Bem-vindo à Auge Invest</h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 mt-2">Sua jornada para o sucesso financeiro começa aqui.</p>
        </header>

        <section className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Placeholder for key features or navigation cards */}
          <div className="bg-white dark:bg-auge-dark-card shadow-lg rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-auge-blue dark:text-white mb-3">Dashboard</h2>
            <p className="text-gray-700 dark:text-gray-400">Acesse seus indicadores e acompanhe o mercado.</p>
          </div>
          <div className="bg-white dark:bg-auge-dark-card shadow-lg rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-auge-blue dark:text-white mb-3">Minha Carteira</h2>
            <p className="text-gray-700 dark:text-gray-400">Gerencie seus investimentos e acompanhe seus rendimentos.</p>
          </div>
          <div className="bg-white dark:bg-auge-dark-card shadow-lg rounded-lg p-6">
            <h2 className="text-2xl font-semibold text-auge-blue dark:text-white mb-3">Análise de Ativos</h2>
            <p className="text-gray-700 dark:text-gray-400">Explore informações detalhadas e tome decisões informadas.</p>
          </div>
        </section>

        {/* TODO: Add more sections like news, blog highlights, etc. */}
      </div>
    </>
  );
}

