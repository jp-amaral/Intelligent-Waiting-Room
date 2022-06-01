import "./App.css";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import PulseMeasurement from "./pages/PulseMeasurement";
import About from "./pages/About";

import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/PulseMeasurement" exact component={PulseMeasurement} />
          <Route path="/about" exact component={About} />

        </Switch>
        
      </Router>
    </div>
  );
}

export default App;
