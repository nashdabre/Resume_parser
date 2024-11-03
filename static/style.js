body {
    background: linear-gradient(135deg, #dceefb, #f0f4f8); /* Soft gradient background */
    font-family: 'Arial', sans-serif;
    color: #333;
    height: 100vh;
}

h1 {
    font-weight: bold;
    color: #007bff;
    text-align: center;
    text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
}

.container {
    margin-top: 50px;
}

form {
    padding: 20px;
    background-color: #ffffff;
    border-radius: 15px;
    box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
}

form:hover {
    box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.15);
}

label {
    font-weight: bold;
    color: #333;
}

input[type="file"] {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    width: 100%;
    box-sizing: border-box;
    background-color: #f7f7f7; /* Light gray background for file inputs */
    color: #555;
    transition: background-color 0.3s ease, border 0.3s ease;
}

input[type="file"]:hover {
    background-color: #e9f0f7; /* Soft blue background on hover */
    border-color: #007bff;
}

button {
    background-color: #007bff;
    color: white;
    padding: 10px;
    font-weight: bold;
    border: none;
    border-radius: 5px;
    width: 100%;
    box-shadow: 0px 5px 10px rgba(0, 123, 255, 0.2);
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

button:hover {
    background-color: #0056b3;
    box-shadow: 0px 7px 15px rgba(0, 123, 255, 0.3);
}

#result h4 {
    color: #28a745;
    font-weight: bold;
}

#loading {
    color: #555;
}

.spinner-border {
    width: 3rem;
    height: 3rem;
    color: #007bff;
}