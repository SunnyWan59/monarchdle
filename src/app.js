import React, { useState, useEffect } from "react";
import axios from "axios";
import "./app.css";

const App = () => {
    const [guess, setGuess] = useState("");
    const [result, setResult] = useState("");
    const [correct, setCorrect] = useState(false);
    

    useEffect(() => {
        if(correct === false) {
        fetchMonarch();
        }
    }, []);


    const fetchMonarch = async () => {
        try{
            const response = await axios.get("/api/monarch");

        } catch (error) {
            console.error("Error fetching monarch:", error);
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
