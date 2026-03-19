import { Column, Entity, PrimaryGeneratedColumn } from "typeorm";
import type { ImportAcData } from "../types/importAcData.js";

@Entity("tb_import_ac_data")
export class ImportAcDataModel implements ImportAcData {
  @PrimaryGeneratedColumn({ name: "coId", type: "bigint" })
  coId!: number;

  @Column({ name: "coCaseId", type: "bigint", nullable: true })
  coCaseId?: number | null;

  // E0I-series
  @Column({ name: "coE0I001", type: "smallint", nullable: true })
  coE0I001?: number | null;

  @Column({ name: "coE0I002", type: "smallint", nullable: true })
  coE0I002?: number | null;

  @Column({ name: "coE0I003", type: "smallint", nullable: true })
  coE0I003?: number | null;

  @Column({ name: "coE0I004", type: "smallint", nullable: true })
  coE0I004?: number | null;

  @Column({
    name: "coE0I005",
    type: "decimal",
    precision: 6,
    scale: 3,
    nullable: true,
  })
  coE0I005?: number | null;

  @Column({ name: "coE0I007", type: "smallint", nullable: true })
  coE0I007?: number | null;

  @Column({ name: "coE0I008", type: "smallint", nullable: true })
  coE0I008?: number | null;

  @Column({ name: "coE0I009", type: "smallint", nullable: true })
  coE0I009?: number | null;

  @Column({ name: "coE0I010", type: "smallint", nullable: true })
  coE0I010?: number | null;

  @Column({ name: "coE0I011", type: "smallint", nullable: true })
  coE0I011?: number | null;

  @Column({ name: "coE0I012", type: "smallint", nullable: true })
  coE0I012?: number | null;

  @Column({ name: "coE0I013", type: "smallint", nullable: true })
  coE0I013?: number | null;

  @Column({ name: "coE0I014", type: "smallint", nullable: true })
  coE0I014?: number | null;

  @Column({ name: "coE0I015", type: "smallint", nullable: true })
  coE0I015?: number | null;

  @Column({ name: "coE0I021", type: "smallint", nullable: true })
  coE0I021?: number | null;

  @Column({ name: "coE0I043", type: "smallint", nullable: true })
  coE0I043?: number | null;

  @Column({ name: "coE0I070", type: "smallint", nullable: true })
  coE0I070?: number | null;

  @Column({ name: "coE0I074", type: "smallint", nullable: true })
  coE0I074?: number | null;

  @Column({ name: "coE0I075", type: "smallint", nullable: true })
  coE0I075?: number | null;

  @Column({ name: "coE0I076", type: "smallint", nullable: true })
  coE0I076?: number | null;

  @Column({ name: "coE0I077", type: "smallint", nullable: true })
  coE0I077?: number | null;

  @Column({ name: "coE0I078", type: "smallint", nullable: true })
  coE0I078?: number | null;

  @Column({ name: "coE0I079", type: "smallint", nullable: true })
  coE0I079?: number | null;

  @Column({ name: "coE0I081", type: "smallint", nullable: true })
  coE0I081?: number | null;

  @Column({ name: "coE0I082", type: "smallint", nullable: true })
  coE0I082?: number | null;

  @Column({ name: "coE0I083", type: "smallint", nullable: true })
  coE0I083?: number | null;

  @Column({ name: "coE0I0116", type: "smallint", nullable: true })
  coE0I0116?: number | null;

  @Column({ name: "coE0I0122", type: "smallint", nullable: true })
  coE0I0122?: number | null;

  @Column({ name: "coE0I0134", type: "smallint", nullable: true })
  coE0I0134?: number | null;

  @Column({ name: "coE0I0141", type: "smallint", nullable: true })
  coE0I0141?: number | null;

  @Column({ name: "coE0I0150", type: "smallint", nullable: true })
  coE0I0150?: number | null;

  @Column({ name: "coE0I0163", type: "smallint", nullable: true })
  coE0I0163?: number | null;

  @Column({ name: "coE0I0168", type: "smallint", nullable: true })
  coE0I0168?: number | null;

  @Column({ name: "coE0I0173", type: "smallint", nullable: true })
  coE0I0173?: number | null;

  @Column({ name: "coE0I0178", type: "smallint", nullable: true })
  coE0I0178?: number | null;

  @Column({ name: "coE0I0190", type: "smallint", nullable: true })
  coE0I0190?: number | null;

  @Column({ name: "coE0I0241", type: "smallint", nullable: true })
  coE0I0241?: number | null;

  @Column({ name: "coE0I0262", type: "smallint", nullable: true })
  coE0I0262?: number | null;

  @Column({ name: "coE0I0266", type: "smallint", nullable: true })
  coE0I0266?: number | null;

  @Column({ name: "coE0I0270", type: "smallint", nullable: true })
  coE0I0270?: number | null;

  @Column({ name: "coE0I0276", type: "smallint", nullable: true })
  coE0I0276?: number | null;

  @Column({ name: "coE0I0004", type: "varchar", length: 512, nullable: true })
  coE0I0004?: string | null;

  @Column({ name: "coE0I0071", type: "smallint", nullable: true })
  coE0I0071?: number | null;

  @Column({ name: "coE0I0077", type: "smallint", nullable: true })
  coE0I0077?: number | null;

  @Column({ name: "coE0I0081", type: "smallint", nullable: true })
  coE0I0081?: number | null;

  // E2I-series
  @Column({ name: "coE2I001", type: "smallint", nullable: true })
  coE2I001?: number | null;

  @Column({ name: "coE2I002", type: "smallint", nullable: true })
  coE2I002?: number | null;

  @Column({ name: "coE2I003", type: "smallint", nullable: true })
  coE2I003?: number | null;

  @Column({ name: "coE2I004", type: "smallint", nullable: true })
  coE2I004?: number | null;

  @Column({ name: "coE2I005", type: "smallint", nullable: true })
  coE2I005?: number | null;

  @Column({ name: "coE2I006", type: "smallint", nullable: true })
  coE2I006?: number | null;

  @Column({ name: "coE2I007", type: "smallint", nullable: true })
  coE2I007?: number | null;

  @Column({ name: "coE2I008", type: "smallint", nullable: true })
  coE2I008?: number | null;

  @Column({ name: "coE2I009", type: "smallint", nullable: true })
  coE2I009?: number | null;

  @Column({ name: "coE2I010", type: "smallint", nullable: true })
  coE2I010?: number | null;

  @Column({ name: "coE2I011", type: "smallint", nullable: true })
  coE2I011?: number | null;

  @Column({ name: "coE2I012", type: "smallint", nullable: true })
  coE2I012?: number | null;

  @Column({ name: "coE2I013", type: "smallint", nullable: true })
  coE2I013?: number | null;

  @Column({ name: "coE2I014", type: "smallint", nullable: true })
  coE2I014?: number | null;

  @Column({ name: "coE2I015", type: "smallint", nullable: true })
  coE2I015?: number | null;

  @Column({ name: "coE2I017", type: "smallint", nullable: true })
  coE2I017?: number | null;

  @Column({ name: "coE2I018", type: "smallint", nullable: true })
  coE2I018?: number | null;

  @Column({ name: "coE2I019", type: "smallint", nullable: true })
  coE2I019?: number | null;

  @Column({ name: "coE2I020", type: "smallint", nullable: true })
  coE2I020?: number | null;

  @Column({ name: "coE2I021", type: "smallint", nullable: true })
  coE2I021?: number | null;

  @Column({ name: "coE2I022", type: "smallint", nullable: true })
  coE2I022?: number | null;

  @Column({ name: "coE2I023", type: "smallint", nullable: true })
  coE2I023?: number | null;

  @Column({ name: "coE2I024", type: "smallint", nullable: true })
  coE2I024?: number | null;

  @Column({ name: "coE2I025", type: "smallint", nullable: true })
  coE2I025?: number | null;

  @Column({ name: "coE2I026", type: "smallint", nullable: true })
  coE2I026?: number | null;

  @Column({ name: "coE2I027", type: "smallint", nullable: true })
  coE2I027?: number | null;

  @Column({ name: "coE2I028", type: "smallint", nullable: true })
  coE2I028?: number | null;

  @Column({ name: "coE2I029", type: "smallint", nullable: true })
  coE2I029?: number | null;

  @Column({ name: "coE2I030", type: "smallint", nullable: true })
  coE2I030?: number | null;

  @Column({ name: "coE2I031", type: "smallint", nullable: true })
  coE2I031?: number | null;

  @Column({ name: "coE2I032", type: "smallint", nullable: true })
  coE2I032?: number | null;

  @Column({ name: "coE2I033", type: "smallint", nullable: true })
  coE2I033?: number | null;

  @Column({ name: "coE2I034", type: "smallint", nullable: true })
  coE2I034?: number | null;

  @Column({ name: "coE2I035", type: "smallint", nullable: true })
  coE2I035?: number | null;

  @Column({ name: "coE2I036", type: "smallint", nullable: true })
  coE2I036?: number | null;

  @Column({ name: "coE2I037", type: "smallint", nullable: true })
  coE2I037?: number | null;

  @Column({ name: "coE2I038", type: "smallint", nullable: true })
  coE2I038?: number | null;

  @Column({ name: "coE2I039", type: "smallint", nullable: true })
  coE2I039?: number | null;

  @Column({ name: "coE2I040", type: "smallint", nullable: true })
  coE2I040?: number | null;

  @Column({ name: "coE2I041", type: "smallint", nullable: true })
  coE2I041?: number | null;

  @Column({ name: "coE2I042", type: "smallint", nullable: true })
  coE2I042?: number | null;

  @Column({ name: "coE2I043", type: "smallint", nullable: true })
  coE2I043?: number | null;

  @Column({ name: "coE2I044", type: "smallint", nullable: true })
  coE2I044?: number | null;

  @Column({ name: "coE2I045", type: "smallint", nullable: true })
  coE2I045?: number | null;

  @Column({ name: "coE2I046", type: "smallint", nullable: true })
  coE2I046?: number | null;

  @Column({ name: "coE2I047", type: "smallint", nullable: true })
  coE2I047?: number | null;

  @Column({ name: "coE2I048", type: "smallint", nullable: true })
  coE2I048?: number | null;

  @Column({ name: "coE2I049", type: "smallint", nullable: true })
  coE2I049?: number | null;

  @Column({ name: "coE2I050", type: "smallint", nullable: true })
  coE2I050?: number | null;

  @Column({ name: "coE2I051", type: "smallint", nullable: true })
  coE2I051?: number | null;

  @Column({ name: "coE2I052", type: "smallint", nullable: true })
  coE2I052?: number | null;

  @Column({ name: "coE2I053", type: "smallint", nullable: true })
  coE2I053?: number | null;

  @Column({ name: "coE2I054", type: "smallint", nullable: true })
  coE2I054?: number | null;

  @Column({ name: "coE2I055", type: "smallint", nullable: true })
  coE2I055?: number | null;

  @Column({ name: "coE2I056", type: "smallint", nullable: true })
  coE2I056?: number | null;

  @Column({ name: "coE2I057", type: "smallint", nullable: true })
  coE2I057?: number | null;

  @Column({ name: "coE2I058", type: "smallint", nullable: true })
  coE2I058?: number | null;

  @Column({ name: "coE2I059", type: "smallint", nullable: true })
  coE2I059?: number | null;

  @Column({ name: "coE2I060", type: "smallint", nullable: true })
  coE2I060?: number | null;

  @Column({ name: "coE2I061", type: "smallint", nullable: true })
  coE2I061?: number | null;

  @Column({ name: "coE2I062", type: "smallint", nullable: true })
  coE2I062?: number | null;

  @Column({ name: "coE2I063", type: "smallint", nullable: true })
  coE2I063?: number | null;

  @Column({ name: "coE2I064", type: "smallint", nullable: true })
  coE2I064?: number | null;

  @Column({ name: "coE2I065", type: "smallint", nullable: true })
  coE2I065?: number | null;

  @Column({ name: "coE2I066", type: "smallint", nullable: true })
  coE2I066?: number | null;

  @Column({ name: "coE2I067", type: "smallint", nullable: true })
  coE2I067?: number | null;

  @Column({ name: "coE2I068", type: "smallint", nullable: true })
  coE2I068?: number | null;

  @Column({ name: "coE2I069", type: "smallint", nullable: true })
  coE2I069?: number | null;

  @Column({ name: "coE2I070", type: "smallint", nullable: true })
  coE2I070?: number | null;

  @Column({ name: "coE2I071", type: "smallint", nullable: true })
  coE2I071?: number | null;

  @Column({ name: "coE2I072", type: "smallint", nullable: true })
  coE2I072?: number | null;

  @Column({ name: "coE2I073", type: "smallint", nullable: true })
  coE2I073?: number | null;

  @Column({ name: "coE2I074", type: "smallint", nullable: true })
  coE2I074?: number | null;

  @Column({ name: "coE2I075", type: "smallint", nullable: true })
  coE2I075?: number | null;

  @Column({ name: "coE2I076", type: "smallint", nullable: true })
  coE2I076?: number | null;

  @Column({ name: "coE2I077", type: "smallint", nullable: true })
  coE2I077?: number | null;

  @Column({ name: "coE2I078", type: "smallint", nullable: true })
  coE2I078?: number | null;

  @Column({ name: "coE2I079", type: "smallint", nullable: true })
  coE2I079?: number | null;

  @Column({ name: "coE2I080", type: "smallint", nullable: true })
  coE2I080?: number | null;

  @Column({ name: "coE2I081", type: "smallint", nullable: true })
  coE2I081?: number | null;

  @Column({ name: "coE2I082", type: "smallint", nullable: true })
  coE2I082?: number | null;

  @Column({ name: "coE2I083", type: "smallint", nullable: true })
  coE2I083?: number | null;

  @Column({ name: "coE2I084", type: "smallint", nullable: true })
  coE2I084?: number | null;

  @Column({ name: "coE2I085", type: "smallint", nullable: true })
  coE2I085?: number | null;

  @Column({ name: "coE2I086", type: "smallint", nullable: true })
  coE2I086?: number | null;

  @Column({ name: "coE2I087", type: "smallint", nullable: true })
  coE2I087?: number | null;

  @Column({ name: "coE2I088", type: "smallint", nullable: true })
  coE2I088?: number | null;

  // E2I varchar fields
  @Column({ name: "coE2I089", type: "varchar", length: 512, nullable: true })
  coE2I089?: string | null;

  @Column({ name: "coE2I090", type: "varchar", length: 512, nullable: true })
  coE2I090?: string | null;

  @Column({ name: "coE2I091", type: "varchar", length: 512, nullable: true })
  coE2I091?: string | null;

  @Column({ name: "coE2I092", type: "varchar", length: 512, nullable: true })
  coE2I092?: string | null;

  @Column({ name: "coE2I093", type: "varchar", length: 512, nullable: true })
  coE2I093?: string | null;

  @Column({ name: "coE2I095", type: "smallint", nullable: true })
  coE2I095?: number | null;

  @Column({ name: "coE2I094", type: "varchar", length: 512, nullable: true })
  coE2I094?: string | null;

  @Column({ name: "coE2I096", type: "varchar", length: 512, nullable: true })
  coE2I096?: string | null;

  @Column({ name: "coE2I097", type: "varchar", length: 512, nullable: true })
  coE2I097?: string | null;

  @Column({ name: "coE2I098", type: "varchar", length: 512, nullable: true })
  coE2I098?: string | null;

  @Column({ name: "coE2I099", type: "varchar", length: 512, nullable: true })
  coE2I099?: string | null;

  @Column({ name: "coE2I100", type: "varchar", length: 512, nullable: true })
  coE2I100?: string | null;

  @Column({ name: "coE2I101", type: "varchar", length: 512, nullable: true })
  coE2I101?: string | null;

  // E2I 102-179
  @Column({ name: "coE2I102", type: "smallint", nullable: true })
  coE2I102?: number | null;

  @Column({ name: "coE2I103", type: "smallint", nullable: true })
  coE2I103?: number | null;

  @Column({ name: "coE2I104", type: "smallint", nullable: true })
  coE2I104?: number | null;

  @Column({ name: "coE2I105", type: "smallint", nullable: true })
  coE2I105?: number | null;

  @Column({ name: "coE2I106", type: "smallint", nullable: true })
  coE2I106?: number | null;

  @Column({ name: "coE2I107", type: "smallint", nullable: true })
  coE2I107?: number | null;

  @Column({ name: "coE2I108", type: "smallint", nullable: true })
  coE2I108?: number | null;

  @Column({ name: "coE2I109", type: "smallint", nullable: true })
  coE2I109?: number | null;

  @Column({ name: "coE2I110", type: "smallint", nullable: true })
  coE2I110?: number | null;

  @Column({ name: "coE2I111", type: "smallint", nullable: true })
  coE2I111?: number | null;

  @Column({ name: "coE2I112", type: "smallint", nullable: true })
  coE2I112?: number | null;

  @Column({ name: "coE2I113", type: "smallint", nullable: true })
  coE2I113?: number | null;

  @Column({ name: "coE2I114", type: "smallint", nullable: true })
  coE2I114?: number | null;

  @Column({ name: "coE2I115", type: "smallint", nullable: true })
  coE2I115?: number | null;

  @Column({ name: "coE2I116", type: "smallint", nullable: true })
  coE2I116?: number | null;

  @Column({ name: "coE2I117", type: "smallint", nullable: true })
  coE2I117?: number | null;

  @Column({ name: "coE2I118", type: "smallint", nullable: true })
  coE2I118?: number | null;

  @Column({ name: "coE2I119", type: "smallint", nullable: true })
  coE2I119?: number | null;

  @Column({ name: "coE2I121", type: "smallint", nullable: true })
  coE2I121?: number | null;

  @Column({ name: "coE2I122", type: "smallint", nullable: true })
  coE2I122?: number | null;

  @Column({ name: "coE2I123", type: "smallint", nullable: true })
  coE2I123?: number | null;

  @Column({ name: "coE2I124", type: "smallint", nullable: true })
  coE2I124?: number | null;

  @Column({ name: "coE2I125", type: "smallint", nullable: true })
  coE2I125?: number | null;

  @Column({ name: "coE2I126", type: "smallint", nullable: true })
  coE2I126?: number | null;

  @Column({ name: "coE2I127", type: "smallint", nullable: true })
  coE2I127?: number | null;

  @Column({ name: "coE2I128", type: "smallint", nullable: true })
  coE2I128?: number | null;

  @Column({ name: "coE2I129", type: "smallint", nullable: true })
  coE2I129?: number | null;

  @Column({ name: "coE2I130", type: "smallint", nullable: true })
  coE2I130?: number | null;

  @Column({ name: "coE2I131", type: "smallint", nullable: true })
  coE2I131?: number | null;

  @Column({ name: "coE2I132", type: "smallint", nullable: true })
  coE2I132?: number | null;

  @Column({ name: "coE2I133", type: "smallint", nullable: true })
  coE2I133?: number | null;

  @Column({ name: "coE2I134", type: "smallint", nullable: true })
  coE2I134?: number | null;

  @Column({ name: "coE2I135", type: "smallint", nullable: true })
  coE2I135?: number | null;

  @Column({ name: "coE2I136", type: "smallint", nullable: true })
  coE2I136?: number | null;

  @Column({ name: "coE2I137", type: "smallint", nullable: true })
  coE2I137?: number | null;

  @Column({ name: "coE2I138", type: "smallint", nullable: true })
  coE2I138?: number | null;

  @Column({ name: "coE2I139", type: "smallint", nullable: true })
  coE2I139?: number | null;

  @Column({ name: "coE2I140", type: "smallint", nullable: true })
  coE2I140?: number | null;

  @Column({ name: "coE2I141", type: "smallint", nullable: true })
  coE2I141?: number | null;

  @Column({ name: "coE2I142", type: "smallint", nullable: true })
  coE2I142?: number | null;

  @Column({ name: "coE2I143", type: "smallint", nullable: true })
  coE2I143?: number | null;

  @Column({ name: "coE2I144", type: "smallint", nullable: true })
  coE2I144?: number | null;

  @Column({ name: "coE2I145", type: "smallint", nullable: true })
  coE2I145?: number | null;

  @Column({ name: "coE2I146", type: "smallint", nullable: true })
  coE2I146?: number | null;

  @Column({ name: "coE2I147", type: "smallint", nullable: true })
  coE2I147?: number | null;

  @Column({ name: "coE2I148", type: "smallint", nullable: true })
  coE2I148?: number | null;

  @Column({ name: "coE2I150", type: "smallint", nullable: true })
  coE2I150?: number | null;

  @Column({ name: "coE2I151", type: "smallint", nullable: true })
  coE2I151?: number | null;

  @Column({ name: "coE2I152", type: "smallint", nullable: true })
  coE2I152?: number | null;

  @Column({ name: "coE2I154", type: "smallint", nullable: true })
  coE2I154?: number | null;

  @Column({ name: "coE2I155", type: "smallint", nullable: true })
  coE2I155?: number | null;

  @Column({ name: "coE2I156", type: "smallint", nullable: true })
  coE2I156?: number | null;

  @Column({ name: "coE2I157", type: "smallint", nullable: true })
  coE2I157?: number | null;

  @Column({ name: "coE2I158", type: "smallint", nullable: true })
  coE2I158?: number | null;

  @Column({ name: "coE2I159", type: "smallint", nullable: true })
  coE2I159?: number | null;

  @Column({ name: "coE2I160", type: "smallint", nullable: true })
  coE2I160?: number | null;

  @Column({ name: "coE2I161", type: "smallint", nullable: true })
  coE2I161?: number | null;

  @Column({ name: "coE2I162", type: "smallint", nullable: true })
  coE2I162?: number | null;

  @Column({ name: "coE2I163", type: "smallint", nullable: true })
  coE2I163?: number | null;

  @Column({ name: "coE2I164", type: "smallint", nullable: true })
  coE2I164?: number | null;

  @Column({ name: "coE2I165", type: "smallint", nullable: true })
  coE2I165?: number | null;

  @Column({ name: "coE2I166", type: "smallint", nullable: true })
  coE2I166?: number | null;

  @Column({ name: "coE2I167", type: "smallint", nullable: true })
  coE2I167?: number | null;

  @Column({ name: "coE2I168", type: "smallint", nullable: true })
  coE2I168?: number | null;

  @Column({ name: "coE2I169", type: "smallint", nullable: true })
  coE2I169?: number | null;

  @Column({ name: "coE2I170", type: "smallint", nullable: true })
  coE2I170?: number | null;

  @Column({ name: "coE2I171", type: "smallint", nullable: true })
  coE2I171?: number | null;

  @Column({ name: "coE2I172", type: "smallint", nullable: true })
  coE2I172?: number | null;

  @Column({ name: "coE2I173", type: "smallint", nullable: true })
  coE2I173?: number | null;

  @Column({ name: "coE2I178", type: "smallint", nullable: true })
  coE2I178?: number | null;

  @Column({ name: "coE2I179", type: "smallint", nullable: true })
  coE2I179?: number | null;

  // E2I 217+
  @Column({ name: "coE2I217", type: "smallint", nullable: true })
  coE2I217?: number | null;

  @Column({ name: "coE2I218", type: "smallint", nullable: true })
  coE2I218?: number | null;

  @Column({ name: "coE2I220", type: "smallint", nullable: true })
  coE2I220?: number | null;

  @Column({ name: "coE2I221", type: "smallint", nullable: true })
  coE2I221?: number | null;

  @Column({ name: "coE2I222", type: "bigint", nullable: true })
  coE2I222?: number | null;

  @Column({ name: "coE2I223", type: "timestamp", nullable: true })
  coE2I223?: Date | null;

  @Column({ name: "coE2I224", type: "smallint", nullable: true })
  coE2I224?: number | null;

  @Column({ name: "coE2I225", type: "timestamp" })
  coE2I225!: Date;

  @Column({ name: "coE2I226", type: "bigint", nullable: true })
  coE2I226?: number | null;

  @Column({ name: "coE2I227", type: "smallint", nullable: true })
  coE2I227?: number | null;

  @Column({ name: "coE2I228", type: "timestamp", nullable: true })
  coE2I228?: Date | null;

  @Column({ name: "coE2I229", type: "smallint", nullable: true })
  coE2I229?: number | null;

  @Column({ name: "coE2I230", type: "varchar", length: 256, nullable: true })
  coE2I230?: string | null;

  @Column({ name: "coE2I231", type: "varchar", length: 256, nullable: true })
  coE2I231?: string | null;

  @Column({ name: "coE2I232", type: "varchar", length: 256, nullable: true })
  coE2I232?: string | null;

  // E2I2-series
  @Column({ name: "coE2I2000", type: "smallint", nullable: true })
  coE2I2000?: number | null;

  @Column({ name: "coE2I2013", type: "smallint", nullable: true })
  coE2I2013?: number | null;

  @Column({ name: "coE2I2022", type: "smallint", nullable: true })
  coE2I2022?: number | null;

  @Column({ name: "coE2I2029", type: "smallint", nullable: true })
  coE2I2029?: number | null;

  @Column({ name: "coE2I2033", type: "smallint", nullable: true })
  coE2I2033?: number | null;

  @Column({ name: "coE2I2092", type: "smallint", nullable: true })
  coE2I2092?: number | null;

  @Column({ name: "coE2I2099", type: "smallint", nullable: true })
  coE2I2099?: number | null;

  @Column({ name: "coE2I2126", type: "smallint", nullable: true })
  coE2I2126?: number | null;

  @Column({ name: "coE2I2134", type: "smallint", nullable: true })
  coE2I2134?: number | null;

  @Column({ name: "coE2I2148", type: "smallint", nullable: true })
  coE2I2148?: number | null;

  @Column({ name: "coE2I2154", type: "smallint", nullable: true })
  coE2I2154?: number | null;

  @Column({ name: "coE2I2157", type: "smallint", nullable: true })
  coE2I2157?: number | null;

  @Column({ name: "coE2I2165", type: "smallint", nullable: true })
  coE2I2165?: number | null;

  @Column({ name: "coE2I2170", type: "smallint", nullable: true })
  coE2I2170?: number | null;

  @Column({ name: "coE2I2175", type: "smallint", nullable: true })
  coE2I2175?: number | null;

  @Column({ name: "coE2I2180", type: "smallint", nullable: true })
  coE2I2180?: number | null;

  @Column({ name: "coE2I2188", type: "smallint", nullable: true })
  coE2I2188?: number | null;

  @Column({ name: "coE2I2191", type: "smallint", nullable: true })
  coE2I2191?: number | null;

  @Column({ name: "coE2I2195", type: "smallint", nullable: true })
  coE2I2195?: number | null;

  @Column({ name: "coE2I2199", type: "smallint", nullable: true })
  coE2I2199?: number | null;

  @Column({ name: "coE2I2203", type: "smallint", nullable: true })
  coE2I2203?: number | null;

  @Column({ name: "coE2I2207", type: "smallint", nullable: true })
  coE2I2207?: number | null;

  @Column({ name: "coE2I2211", type: "smallint", nullable: true })
  coE2I2211?: number | null;

  @Column({ name: "coE2I2216", type: "smallint", nullable: true })
  coE2I2216?: number | null;

  @Column({ name: "coE2I2222", type: "smallint", nullable: true })
  coE2I2222?: number | null;

  @Column({ name: "coE2I2256", type: "smallint", nullable: true })
  coE2I2256?: number | null;

  @Column({ name: "coE2I2267", type: "smallint", nullable: true })
  coE2I2267?: number | null;

  @Column({ name: "coE2I2279", type: "smallint", nullable: true })
  coE2I2279?: number | null;

  // Extra fields
  @Column({ name: "coMaxDekuGrad", type: "smallint", nullable: true })
  coMaxDekuGrad?: number | null;

  @Column({ name: "coDekubitusWertTotal", type: "smallint", nullable: true })
  coDekubitusWertTotal?: number | null;

  @Column({ name: "coLastAssessment", type: "smallint", nullable: true })
  coLastAssessment?: number | null;

  @Column({ name: "coE3I0889", type: "varchar", length: 256, nullable: true })
  coE3I0889?: string | null;

  @Column({
    name: "coCaseIdAlpha",
    type: "varchar",
    length: 256,
    nullable: true,
  })
  coCaseIdAlpha?: string | null;
}
