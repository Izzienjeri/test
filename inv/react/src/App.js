import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const PageB = () => {
  const [count, setCount] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [hasGameEnded, setHasGameEnded] = useState(false);
  const [remainingTime, setRemainingTime] = useState(10);
  const [progress, setProgress] = useState(100);
  const timerIdRef = useRef();

  // Countdown logic
  useEffect(() => {
    if (isRunning) {
      const intervalId = setInterval(() => {
        setRemainingTime((prevTime) => prevTime - 1);
      }, 1000);
      return () => clearInterval(intervalId);
    }
  }, [isRunning]);

  // Title and game end logic
  useEffect(() => {
    document.title = isRunning
      ? `Time Remaining: ${remainingTime}`
      : `You clicked ${count} times!`;

    if (remainingTime === 0) {
      setIsRunning(false);
      setHasGameEnded(true);
    }

    setProgress((remainingTime / 10) * 100);
  }, [remainingTime, isRunning, count]);

  // Handle button click
  const handleClick = () => {
    if (!hasGameEnded && !isRunning) {
      setIsRunning(true);
      setTimeout(() => {
        setIsRunning(false);
        setHasGameEnded(true);
      }, 10000);
    }

    if (isRunning) {
      setCount((prev) => prev + 1);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen w-screen bg-gray-100 relative">

      {/* Progress Bar */}
      <div className="w-full h-4 rounded-full overflow-hidden bg-gray-300 absolute top-0">
        <div
          className="progress-bar"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Game Box */}
      <div className="bg-white rounded-lg shadow-md p-8 z-10 mt-8">
        <h1 className="text-4xl font-bold mb-8">Clicking in 10 Seconds Game</h1>

        <div className="flex items-center space-x-4">
          <div className="bg-blue-500 text-white font-semibold rounded-full w-48 h-48 flex items-center justify-center text-2xl">
            {isRunning ? remainingTime : 'Time Up!'}
          </div>

          <button
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded font-bold"
            onClick={handleClick}
          >
            Click Me
          </button>
        </div>

        <p className="text-2xl mt-4">Count: {count}</p>
      </div>
    </div>
  );
};

export default PageB;

