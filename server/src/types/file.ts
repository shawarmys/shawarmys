export interface IFile {
  id: number;
  name: string;
  groupType: string;
  source: string;
  entries: number;
  records: number;
  type: string;
  createdAt: Date;
}
