import { DataSource } from "typeorm";

const dbUrl = process.env.DATABASE_URL;
console.log(
  "Using database URL:",
  dbUrl ? "****" : "not set, using individual DB_* vars",
);

const AppDataSource = new DataSource({
  type: "postgres",
  // prefer a single DATABASE_URL (used in docker-compose). Fall back to individual vars.
  url: dbUrl ?? undefined,
  host: process.env.DB_HOST ?? "localhost",
  port: Number(process.env.DB_PORT ?? 5432),
  username: process.env.DB_USER ?? process.env.POSTGRES_USER,
  password: process.env.DB_PASSWORD ?? process.env.POSTGRES_PASSWORD,
  database: process.env.DB_NAME ?? process.env.POSTGRES_DB,
  entities: [__dirname + "/../models/*.{ts,js}"],
  synchronize: false,
  logging: false,
});

/**
 * Initialize and return the TypeORM DataSource.
 * Call this once on application startup (for example in server bootstrap).
 */
export async function initializeDataSource(): Promise<DataSource> {
  if (!AppDataSource.isInitialized) {
    try {
      await AppDataSource.initialize();
      console.log("Data Source has been initialized!");
    } catch (error) {
      console.error("Error during Data Source initialization", error);
      throw error;
    }
  }
  return AppDataSource;
}

/**
 * Returns the initialized DataSource. Throws if not initialized yet.
 */
export function getDB(): DataSource {
  if (!AppDataSource.isInitialized) {
    throw new Error(
      "DataSource not initialized. Call initializeDataSource() first.",
    );
  }
  return AppDataSource;
}
