const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const session = require("express-session");

// Connect to MongoDB
mongoose.connect("mongodb://localhost:27017/registrationDB", { useNewUrlParser: true, useUnifiedTopology: true });

// Define User Schema
const userSchema = new mongoose.Schema({
    username: String,
    email: String,
    age: Number,
    occupation: String,
    nationality: String,
    county: String,
    interests: String,
    password: String,
});

// User Model
const User = mongoose.model("User", userSchema);

const app = express();

// Middleware
app.use(bodyParser.json());
app.use(session({
    secret: "your-secret-key",
    resave: false,
    saveUninitialized: true,
}));

// Registration Endpoint
app.post("/submit_registration", async (req, res) => {
    const { username, email, age, occupation, nationality, county, interests, password } = req.body;

    try {
        // Check if user already exists
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ success: false, message: "Email already in use." });
        }

        // Hash the password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create and save the user
        const newUser = new User({
            username,
            email,
            age,
            occupation,
            nationality,
            county,
            interests,
            password: hashedPassword,
        });

        await newUser.save();

        // Set session
        req.session.userId = newUser._id;

        res.json({ success: true, message: "Registration successful!" });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: "Server error. Please try again." });
    }
});

// Dashboard (Example Protected Route)
app.get("/dashboard", (req, res) => {
    if (!req.session.userId) {
        return res.status(401).send("Unauthorized. Please log in.");
    }
    res.send("Welcome to your dashboard!");
});

// Start Server
app.listen(3000, () => console.log("Server running on http://localhost:3000"));