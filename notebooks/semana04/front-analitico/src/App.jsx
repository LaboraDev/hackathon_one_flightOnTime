import FlightForm from "./components/form/FlightForm";
import Dashboard from "./components/dashboard/Dashboard";

function App() {
  return (
    <div className="app-container">
      <header
        style={{
          position: "relative",
          top: 30,
          left: 40,
          color: "#ffffff",
          opacity: 0.9,
        }}
      >
        <h2 style={{ margin: 0 }}>FlightPredict</h2>
        <small>AI-powered delay analysis</small>
      </header>

      <main>
        {/* Formulário de entrada */}
        <section>
          <FlightForm />
        </section>

        {/* Futuras seções */}
        {
          <>
            <Dashboard />
          </> /*
        <section>
          <Dashboard />
        </section>

        <section>
          <ModelExplainability />
        </section>
        */
        }
      </main>
    </div>
  );
}

export default App;
