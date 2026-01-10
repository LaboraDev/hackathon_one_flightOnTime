import FlightForm from "./components/form/FlightForm";

function App() {
  return (
    <div className="app-container">
      <header>
        <h1>Flight Delay Prediction</h1>
        <p>Análise preditiva de atrasos de voos</p>
      </header>

      <main>
        {/* Formulário de entrada */}
        <section>
          <FlightForm />
        </section>

        {/* Futuras seções */}
        {/*
        <section>
          <Dashboard />
        </section>

        <section>
          <ModelExplainability />
        </section>
        */}
      </main>
    </div>
  );
}

export default App;
