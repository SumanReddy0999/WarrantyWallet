import 'dotenv/config'; // Must be the first line
import express from 'express';
import cors from 'cors';
import { storage } from './storage'; // Assuming storage.ts is in the same directory

const app = express();
const port = 5000; // Define the port for the auth-service

// --- Middleware ---
app.use(cors()); // Enable CORS for all routes
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// --- API Routes ---

// User signup endpoint
app.post("/api/signup", async (req, res, next) => {
    try {
        const { firstName, lastName, email, phone, password } = req.body;
        if (!email || !password || !firstName || !lastName) {
            return res.status(400).json({ message: "Missing required fields." });
        }
        const userData = {
            fullName: `${firstName} ${lastName}`,
            email,
            phoneNumber: phone,
            password,
            authProvider: 'email_password',
        };
        const newUser = await storage.createUser(userData);
        const userResponse = {
            id: newUser.id,
            email: newUser.email,
            fullName: newUser.fullName,
        };
        res.status(201).json(userResponse);
    } catch (error: any) {
        if (error.code === '23505') {
             error.message = 'A user with this email already exists.';
             res.status(409);
        }
        next(error);
    }
});

// User login endpoint
app.post("/api/login", async (req, res, next) => {
    try {
        const { email, password } = req.body;
        if (!email || !password) {
            return res.status(400).json({ message: "Email and password are required." });
        }
        const user = await storage.verifyUser(email, password);
        res.status(200).json({
            id: user.id,
            email: user.email,
            fullName: user.fullName,
        });
    } catch (error: any) {
        res.status(401);
        next(error);
    }
});

// --- Start Server ---
app.listen(port, () => {
  console.log(`[auth-service] running on http://localhost:${port}`);
});