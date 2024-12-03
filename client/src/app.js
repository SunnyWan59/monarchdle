import React, { useState, useEffect } from "react";
import axios from "axios";
import "./app.css";

const emptyMonarch = {
    name: "None",
    portrait: "None",
    start_year: "TEST",
    end_year: "None",
    reign_time: "None",
    country: "None"
}


const App = () => {
    const [guess, setGuess] = useState("");
    const [result, setResult] = useState("");
    const [correct, setCorrect] = useState(false);
    const [monarch, setMonarch] = useState(emptyMonarch);

    // useEffect(() => {
    //     console.log(`Monarch type: ${typeof monarch}`);
    //     console.log(`Monarch name: ${monarch.name}`);
    // }, [monarch]);


    /*
    All of this here is a sanity check to make sure everything is conencted.
    */
    const [data, setData] = useState([{}]);
    useEffect(() => {
        fetch("api/test")
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error("Error fetching data:", error));
    });

    useEffect(() => {
        if (monarch.name === "None") {
            console.log("Monarch is None");
            initializeMonarch();
        } 
    }, []);

    const initializeMonarch = async () => {
        try {
            // const response = await axios.post("/api/monarch");
            const response = await axios.get("/api/monarch");
        } catch (error) {
            console.error("Error setting monarch:", error);
        }
    };



    const submitGuess = async () => {
        try {
            const response = await axios.post("/api/guess", { guess });
            if (response.data.correct) {
            setResult(`Correct! The champion was ${response.data.champion}.`);
            setCorrect(true);
            } else {
            setResult("Incorrect! Try again.");
            }
        } catch (error) {
            console.error("Error submitting guess:", error);
        }
    };

    const restartGame = async () => {
        try {
            await axios.post("/api/restart");
        } catch (error) {
            console.error("Error restarting game:", error);
        }
    };

    return (
        <div className="App">
            <header>
            <h1>Monarchdle</h1>
            </header>
            <input
            type="text"
            placeholder="Enter monarch name"
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
            disabled={correct}
            />
            <button onClick={submitGuess} disabled={correct}>
            Submit Guess
            </button>
            <button onClick={restartGame}>Restart Game</button>
            
            <p>{result}</p>
        </div>
    );
};

export default App;
