export type EvidenceStatus =
  | "production_verified"
  | "shipped_unverified"
  | "in_progress"
  | "pending"
  | "planned";

export type CommsItem = {
  status: EvidenceStatus;
  title: string;
  detail: string;
  evidence_ids: string[];
};

export type CommsSection = {
  title: string;
  items: CommsItem[];
};

export type CommsBag = {
  schema_version: 1;
  id: string;
  kind: "project_update" | "internal_digest";
  generated_at: string;
  subject: string;
  preheader: string;
  audience_id: string;
  project_ids: string[];
  summary: string;
  sections: CommsSection[];
};
