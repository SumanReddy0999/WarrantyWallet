import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import multer from "multer";
import path from "path";
import fs from "fs";
import { nanoid } from "nanoid";
import { insertWarrantyDocumentSchema } from "shared-types";

// Create uploads directory if it doesn't exist
const uploadsDir = path.join(process.cwd(), "uploads");
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// Configure multer for file uploads
const storage_multer = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadsDir);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${nanoid()}-${file.originalname}`;
    cb(null, uniqueName);
  },
});

const upload = multer({
  storage: storage_multer,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    // Allow common document types
    const allowedTypes = [
      'application/pdf',
      'image/jpeg',
      'image/png',
      'image/jpg',
      'text/plain',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];
    
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      const error = new Error('File type not supported') as any;
      cb(error, false);
    }
  },
});

export async function registerRoutes(app: Express): Promise<Server> {
  
  // Document upload endpoint
  app.post("/api/documents/upload", upload.single("document"), async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ error: "No file uploaded" });
      }

      // For now, use a test user UUID (we'll implement proper auth later)
      const testUserId = "01234567-89ab-cdef-0123-456789abcdef"; // Example UUID

      const documentData = {
        userId: testUserId,
        fileName: req.file.filename,
        fileType: req.file.mimetype,
        fileUrl: req.file.path, // Using local path for now
        productName: null,
        brand: null,
        purchaseDate: null,
        warrantyExpiry: null,
        metadata: {
          originalName: req.file.originalname,
          fileSize: req.file.size,
          uploadPath: req.file.path,
        },
      };

      const validatedData = insertWarrantyDocumentSchema.parse(documentData);
      const document = await storage.createWarrantyDocument(validatedData);

      res.json({
        success: true,
        document: {
          id: document.id,
          fileName: document.fileName,
          productName: document.productName,
          brand: document.brand,
          createdAt: document.createdAt,
          metadata: document.metadata,
        },
      });
    } catch (error) {
      console.error("Upload error:", error);
      res.status(500).json({ error: "Failed to upload document" });
    }
  });

  // Get user documents
  app.get("/api/documents", async (req, res) => {
    try {
      // For now, use a test user UUID (we'll implement proper auth later)
      const testUserId = "01234567-89ab-cdef-0123-456789abcdef";
      const documents = await storage.getWarrantyDocumentsByUserId(testUserId);
      
      res.json({
        success: true,
        documents: documents.map((doc) => ({
          id: doc.id,
          fileName: doc.fileName,
          productName: doc.productName,
          brand: doc.brand,
          purchaseDate: doc.purchaseDate,
          warrantyExpiry: doc.warrantyExpiry,
          createdAt: doc.createdAt,
          metadata: doc.metadata,
        })),
      });
    } catch (error) {
      console.error("Get documents error:", error);
      res.status(500).json({ error: "Failed to fetch documents" });
    }
  });

  // Update document metadata
  app.patch("/api/documents/:id", async (req, res) => {
    try {
      const documentId = req.params.id;
      const { productName, brand, purchaseDate, warrantyExpiry } = req.body;
      
      const updates = {
        productName,
        brand,
        purchaseDate: purchaseDate || null,
        warrantyExpiry: warrantyExpiry || null,
      };

      const document = await storage.updateWarrantyDocument(documentId, updates);
      
      if (!document) {
        return res.status(404).json({ error: "Document not found" });
      }

      res.json({ success: true, document });
    } catch (error) {
      console.error("Update document error:", error);
      res.status(500).json({ error: "Failed to update document" });
    }
  });

  // Delete document
  app.delete("/api/documents/:id", async (req, res) => {
    try {
      const documentId = req.params.id;
      const document = await storage.getWarrantyDocumentById(documentId);
      
      if (!document) {
        return res.status(404).json({ error: "Document not found" });
      }

      // Delete file from disk if it exists
      const filePath = document.fileUrl;
      if (filePath && fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
      }

      // Delete associated chunks first (cascade should handle this but let's be explicit)
      await storage.deleteDocumentChunksByDocumentId(documentId);
      
      // Delete from database
      await storage.deleteWarrantyDocument(documentId);

      res.json({ success: true, message: "Document deleted successfully" });
    } catch (error) {
      console.error("Delete document error:", error);
      res.status(500).json({ error: "Failed to delete document" });
    }
  });

  // User signup endpoint
  app.post("/api/signup", async (req, res, next) => {
    try {
      const { firstName, lastName, email, phone, address, password } = req.body;

      // Basic validation
      if (!email || !password || !firstName || !lastName) {
        return res.status(400).json({ message: "Missing required fields." });
      }

      const userData = {
        fullName: `${firstName} ${lastName}`,
        email,
        phoneNumber: phone,
        address, // Note: Your schema doesn't have an address field. You may want to add it.
        password, // The password will be hashed in the storage layer
        authProvider: 'email_password',
      };

      const newUser = await storage.createUser(userData);

      // Don't send the password back in the response
      const userResponse = {
        id: newUser.id,
        email: newUser.email,
        fullName: newUser.fullName,
      };

      res.status(201).json(userResponse);
    } catch (error: any) {
        // Handle cases where the email might already exist
        if (error.code === '23505') { // PostgreSQL unique violation error code
             error.message = 'A user with this email already exists.';
             res.status(409); // 409 Conflict
        }
        next(error); // Pass other errors to the global error handler
    }
  });

  // User login endpoint
  app.post("/api/login", async (req, res, next) => {
    try {
      const { email, password } = req.body;

      // Basic validation
      if (!email || !password) {
        return res.status(400).json({ message: "Email and password are required." });
      }

      // Verify user credentials
      const user = await storage.verifyUser(email, password);
      
      // On successful login, you would typically create a session/token.
      // For now, we'll just return the user info (excluding password hash).
      res.status(200).json({
        id: user.id,
        email: user.email,
        fullName: user.fullName,
      });

    } catch (error: any) {
      // Pass errors (like "Invalid credentials") to the global error handler
      // Set a specific status code for authentication failure
      res.status(401); // 401 Unauthorized
      next(error);
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
