import { pgTable, uuid, text, timestamp, date, jsonb, bigserial, bigint, vector } from "drizzle-orm/pg-core";
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
    id: uuid("id").primaryKey().defaultRandom(),
    name: text("name").unique().notNull(),
});

// --- Manufacturers table ---
export const manufacturers = pgTable("manufacturers", {
    id: uuid("id").primaryKey().defaultRandom(),
    name: text("name").notNull().unique(),
    contactInfo: jsonb("contact_info"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Products table ---
export const products = pgTable("products", {
    id: uuid("id").primaryKey().defaultRandom(),
    manufacturerId: uuid("manufacturer_id").references(() => manufacturers.id, { onDelete: "cascade" }).notNull(),
    name: text("name").notNull(),
    modelNumber: text("model_number"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Warranties table ---
export const warranties = pgTable("warranties", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    categoryId: uuid("category_id").references(() => categories.id),
    productId: uuid("product_id").references(() => products.id, { onDelete: "set null" }),
    originalFilename: text("original_filename").notNull(),
    storagePath: text("storage_path").notNull(),
    fileMimeType: text("file_mime_type"),
    uploadStatus: text("upload_status").default('processing').notNull(),
    serialNumber: text("serial_number"),
    warrantyNumber: text("warranty_number"),
    purchaseDate: date("purchase_date"),
    expiryDate: date("expiry_date"),
    retailerName: text("retailer_name"),
    additionalMetadata: jsonb("additional_metadata"),
    uploadedAt: timestamp("uploaded_at").defaultNow().notNull(),
});

// --- Document Chunks table ---
export const documentChunks = pgTable("document_chunks", {
    id: uuid("id").primaryKey().defaultRandom(),
    warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
    chunkText: text("chunk_text").notNull(),
    vector: vector("vector", { dimensions: 768 }),
    metadata: jsonb("metadata"),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Chat Sessions & Messages ---
export const chatSessions = pgTable("chat_sessions", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const chatMessages = pgTable("chat_messages", {
    id: uuid("id").primaryKey().defaultRandom(),
    sessionId: uuid("session_id").references(() => chatSessions.id, { onDelete: "cascade" }).notNull(),
    senderType: text("sender_type").notNull(),
    content: text("content").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Notifications ---
export const notifications = pgTable("notifications", {
    id: uuid("id").primaryKey().defaultRandom(),
    userId: uuid("user_id").references(() => users.id, { onDelete: "cascade" }).notNull(),
    warrantyId: uuid("warranty_id").references(() => warranties.id, { onDelete: "cascade" }).notNull(),
    notificationType: text("notification_type").notNull(),
    content: text("content").notNull(),
    status: text("status").default('created').notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
});

// --- Table Relations ---
export const manufacturerRelations = relations(manufacturers, ({ many }) => ({
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