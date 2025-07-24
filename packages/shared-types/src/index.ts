import { pgTable, uuid, text, timestamp, date, jsonb, serial, bigserial, integer } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";
import { relations } from "drizzle-orm";

// --- Users table ---
export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  fullName: text("full_name"),
  email: text("email").unique().notNull(),
  phoneNumber: text("phone_number").unique(),
  passwordHash: text("password_hash"),
  authProvider: text("auth_provider").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

// --- Categories table ---
export const categories = pgTable("categories", {
    id: serial("id").primaryKey(),
    name: text("name").unique().notNull(),
});

// --- Warranties table ---
export const warranties = pgTable("warranties", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    categoryId: integer("category_id").references(() => categories.id),
    originalFilename: text("original_filename").notNull(),
    storagePath: text("storage_path").notNull(),
    fileMimeType: text("file_mime_type"),
    uploadStatus: text("upload_status").default('processing').notNull(),
    productName: text("product_name"),
    modelNumber: text("model_number"),
    serialNumber: text("serial_number"),
    warrantyNumber: text("warranty_number"),
    purchaseDate: date("purchase_date"),
    expiryDate: date("expiry_date"),
    retailerName: text("retailer_name"),
    additionalMetadata: jsonb("additional_metadata"),
    uploadedAt: timestamp("uploaded_at").defaultNow().notNull(),
});

// --- Chat Sessions table ---
export const chatSessions = pgTable("chat_sessions", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Chat Messages table ---
export const chatMessages = pgTable("chat_messages", {
    id: bigserial("id", { mode: "number" }).primaryKey(),
    sessionId: uuid("session_id").references(() => chatSessions.id, { onDelete: "cascade" }).notNull(),
    senderType: text("sender_type").notNull(), // 'user' or 'ai'
    content: text("content").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Notifications table ---
export const notifications = pgTable("notifications", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
    notificationType: text("notification_type").notNull(),
    content: text("content").notNull(),
    status: text("status").default('created').notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Document Chunks table (renamed from warranty_documents) ---
export const documentChunks = pgTable("document_chunks", {
  id: uuid("id").primaryKey().defaultRandom(),
  warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
  chunkText: text("chunk_text").notNull(),
  // embedding: vector("embedding", { dimensions: 1536 }), // Add when pgvector is configured
  metadata: jsonb("metadata"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Zod Schemas and Types (You can add these as needed) ---
export const insertUserSchema = createInsertSchema(users);
export type User = typeof users.$inferSelect;