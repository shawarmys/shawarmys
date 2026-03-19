import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";
import type { IFile } from "../types/file.js";

@Entity("files")
export class File implements IFile {
  @PrimaryGeneratedColumn({ type: "bigint" })
  id!: number;

  @Column({ type: "varchar", length: 512 })
  name!: string;

  @Column({ name: "group_type", type: "varchar", length: 256 })
  groupType!: string;

  @Column({ type: "varchar", length: 256 })
  source!: string;

  @Column({ type: "int" })
  entries!: number;

  @Column({ type: "int" })
  records!: number;

  @Column({ type: "varchar", length: 16 })
  type!: string;

  @Column({ name: "created_at", type: "timestamp", default: () => "NOW()" })
  createdAt!: Date;
}
