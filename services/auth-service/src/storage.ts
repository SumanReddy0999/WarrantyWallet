import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import { 
  users, 
  warrantyDocuments, 
  documentChunks,
  type User, 
  type InsertUser, 
  type WarrantyDocument, 
  type InsertWarrantyDocument,
  type DocumentChunk,
  type InsertDocumentChunk 
} from "shared-types";
import { eq } from "drizzle-orm";
import bcrypt from 'bcryptjs';

// Database connection
const connectionString = process.env.DATABASE_URL!;
const client = postgres(connectionString);
const db = drizzle(client);

export interface IStorage {
  // User operations
  getUser(id: string): Promise<User | undefined>;
  getUserByEmail(email: string): Promise<User | undefined>;
  createUser(user: any): Promise<User>;
  verifyUser(email: string, password: string): Promise<User>; // Added for login
  
  // Warranty Document operations
  createWarrantyDocument(document: InsertWarrantyDocument): Promise<WarrantyDocument>;
  getWarrantyDocumentsByUserId(userId: string): Promise<WarrantyDocument[]>;
  getWarrantyDocumentById(id: string): Promise<WarrantyDocument | undefined>;
  deleteWarrantyDocument(id: string): Promise<void>;
  updateWarrantyDocument(id: string, updates: Partial<InsertWarrantyDocument>): Promise<WarrantyDocument | undefined>;
  
  // Document Chunk operations
  createDocumentChunk(chunk: InsertDocumentChunk): Promise<DocumentChunk>;
  getDocumentChunksByDocumentId(documentId: string): Promise<DocumentChunk[]>;
  deleteDocumentChunksByDocumentId(documentId: string): Promise<void>;
}

export class DatabaseStorage implements IStorage {
  // --- USER OPERATIONS ---
  async getUser(id: string): Promise<User | undefined> {
    const result = await db.select().from(users).where(eq(users.id, id));
    return result[0];
  }

  async getUserByEmail(email: string): Promise<User | undefined> {
    const result = await db.select().from(users).where(eq(users.email, email));
    return result[0];
  }

  async createUser(userData: any): Promise<User> {
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(userData.password, saltRounds);
    const newUserPayload = {
      fullName: userData.fullName,
      email: userData.email,
      phoneNumber: userData.phoneNumber,
      authProvider: userData.authProvider,
      passwordHash: hashedPassword,
    };
    const result = await db.insert(users).values(newUserPayload).returning();
    return result[0];
  }

  async verifyUser(email: string, password: string): Promise<User> {
    const user = await this.getUserByEmail(email);
    if (!user || !user.passwordHash) {
      throw new Error("Invalid email or password.");
    }
    const isPasswordValid = await bcrypt.compare(password, user.passwordHash);
    if (!isPasswordValid) {
      throw new Error("Invalid email or password.");
    }
    return user;
  }

  // --- WARRANTY DOCUMENT OPERATIONS ---
  async createWarrantyDocument(insertDocument: InsertWarrantyDocument): Promise<WarrantyDocument> {
    const result = await db.insert(warrantyDocuments).values(insertDocument).returning();
    return result[0];
  }

  async getWarrantyDocumentsByUserId(userId: string): Promise<WarrantyDocument[]> {
    return await db.select().from(warrantyDocuments).where(eq(warrantyDocuments.userId, userId));
  }

  async getWarrantyDocumentById(id: string): Promise<WarrantyDocument | undefined> {
    const result = await db.select().from(warrantyDocuments).where(eq(warrantyDocuments.id, id));
    return result[0];
  }

  async updateWarrantyDocument(id: string, updates: Partial<InsertWarrantyDocument>): Promise<WarrantyDocument | undefined> {
    const result = await db.update(warrantyDocuments)
      .set(updates)
      .where(eq(warrantyDocuments.id, id))
      .returning();
    return result[0];
  }

  async deleteWarrantyDocument(id: string): Promise<void> {
    await db.delete(warrantyDocuments).where(eq(warrantyDocuments.id, id));
  }

  // --- DOCUMENT CHUNK OPERATIONS ---
  async createDocumentChunk(insertChunk: InsertDocumentChunk): Promise<DocumentChunk> {
    const result = await db.insert(documentChunks).values(insertChunk).returning();
    return result[0];
  }

  async getDocumentChunksByDocumentId(documentId: string): Promise<DocumentChunk[]> {
    return await db.select().from(documentChunks).where(eq(documentChunks.documentId, documentId));
  }

  async deleteDocumentChunksByDocumentId(documentId: string): Promise<void> {
    await db.delete(documentChunks).where(eq(documentChunks.documentId, documentId));
  }
}

export const storage = new DatabaseStorage();