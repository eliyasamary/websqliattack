import React, { useState } from "react";
import "./App.css";

function Login() {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const validateInput = (input) => {
    const regex = /^[a-zA-Z0-9_]+$/;
    return regex.test(input);
  };

  const escapeInput = (input) => {
    return input.replace(/[\\"']/g, "\\$&").replace(/\u0000/g, "\\0");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    if (!validateInput(userName) || !validateInput(password)) {
      setMessage("Invalid input.");
      return;
    }

    const escapedUserName = escapeInput(userName);
    const escapedPassword = escapeInput(password);

    try {
      const response = await fetch("http://localhost:8080/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userName: escapedUserName,
          password: escapedPassword,
        }),
      });

      if (!response.ok) {
        throw new Error("Login failed");
      }

      const data = await response.json();
      setMessage("Login successful!");
    } catch (error) {
      console.error("Error:", error);
      setMessage("Login failed. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
        <div className="form-group">
          <label>User Name:</label>
          <input
            type="text"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Login</button>
        {message && <p>{message}</p>}
      </form>
    </div>
  );
}

export default Login;