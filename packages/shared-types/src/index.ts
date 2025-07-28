import { pgTable, uuid, text, timestamp, date, jsonb, serial, bigserial, integer, vector } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";
import { relations } from "drizzle-orm";

// --- Users table (No changes) ---
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

// --- Categories table (No changes) ---
export const categories = pgTable("categories", {
    id: serial("id").primaryKey(),
    name: text("name").unique().notNull(),
});

// --- NEW: Manufacturers table ---
export const manufacturers = pgTable("manufacturers", {
    id: uuid("id").primaryKey().defaultRandom(),
    name: text("name").notNull().unique(),
    contactInfo: jsonb("contact_info"), // Store phone, email, website etc.
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- NEW: Products table ---
export const products = pgTable("products", {
    id: uuid("id").primaryKey().defaultRandom(),
    manufacturerId: uuid("manufacturer_id").references(() => manufacturers.id, { onDelete: "cascade" }).notNull(),
    name: text("name").notNull(),
    modelNumber: text("model_number"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- UPDATED: Warranties table ---
export const warranties = pgTable("warranties", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    categoryId: integer("category_id").references(() => categories.id),
    // NEW: Link to the products table
    productId: uuid("product_id").references(() => products.id, { onDelete: "set null" }),
    originalFilename: text("original_filename").notNull(),
    storagePath: text("storage_path").notNull(),
    fileMimeType: text("file_mime_type"),
    uploadStatus: text("upload_status").default('processing').notNull(),
    // REMOVED: productName and modelNumber are now in the products table
    serialNumber: text("serial_number"),
    warrantyNumber: text("warranty_number"),
    purchaseDate: date("purchase_date"),
    expiryDate: date("expiry_date"),
    retailerName: text("retailer_name"),
    additionalMetadata: jsonb("additional_metadata"),
    uploadedAt: timestamp("uploaded_at").defaultNow().notNull(),
});


// --- UPDATED: Document Chunks table ---
export const documentChunks = pgTable("document_chunks", {
    id: uuid("id").primaryKey().defaultRandom(),
    warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
    chunkText: text("chunk_text").notNull(),
    // NEW: Vector column for pgvector embeddings. Dimension matches our Python config.
    vector: vector("vector", { dimensions: 768 }),
    metadata: jsonb("metadata"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});


// --- Chat Sessions & Messages (No changes) ---
export const chatSessions = pgTable("chat_sessions", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const chatMessages = pgTable("chat_messages", {
    id: bigserial("id", { mode: "number" }).primaryKey(),
    sessionId: uuid("session_id").references(() => chatSessions.id, { onDelete: "cascade" }).notNull(),
    senderType: text("sender_type").notNull(),
    content: text("content").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Notifications (No changes) ---
export const notifications = pgTable("notifications", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
    notificationType: text("notification_type").notNull(),
    content: text("content").notNull(),
    status: text("status").default('created').notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});


// --- NEW AND UPDATED: Table Relations ---
// This section tells Drizzle how the tables are connected.

export const manufacturerRelations = relations(manufacturers, ({ one, many }) => ({
    products: many(products),
}));

export const productRelations = relations(products, ({ one, many }) => ({
    manufacturer: one(manufacturers, {
        fields: [products.manufacturerId],
        references: [manufacturers.id],
    }),
    warranties: many(warranties),
}));

export const warrantyRelations = relations(warranties, ({ one, many }) => ({
    user: one(users, {
        fields: [warranties.userId],
        references: [users.id],
    }),
    product: one(products, {
        fields: [warranties.productId],
        references: [products.id],
    }),
    category: one(categories, {
        fields: [warranties.categoryId],
        references: [categories.id],
    }),
    documentChunks: many(documentChunks),
    chatSessions: many(chatSessions),
    notifications: many(notifications),
}));

export const userRelations = relations(users, ({ many }) => ({
    warranties: many(warranties),
    chatSessions: many(chatSessions),
    notifications: many(notifications),
}));

// --- Zod Schemas and Types ---
export const insertUserSchema = createInsertSchema(users);
export type User = typeof users.$inferSelect;
// Add other schemas and types as needed
