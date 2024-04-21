import logo from "./logo.svg";
import "./App.css";
import React, { useState, useEffect } from 'react';
import { SpeedInsights } from "@vercel/speed-insights/react"

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch("https://iris-ashen.vercel.app/full");
      const data = await response.json();
      setData(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };
  return (
    <div className="App">
      <header className="App-header">
        {data ? (
          <div>
            {data}
            {/* Example: <p>{data.someField}</p> */}
            <SpeedInsights />
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </header>
    </div>
  );
}

export default App;
