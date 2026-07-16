export type EvidenceStatus =
  | "production_verified"
  | "shipped_unverified"
  | "in_progress"
  | "pending"
  | "planned";

export type RelayItem = {
  status: EvidenceStatus;
  title: string;
  detail: string;
  evidence_ids: string[];
  visibility?: "client_facing" | "internal";
};

export type RelaySection = { title: string; subtitle?: string; items: RelayItem[] };
export type RelayBag = {
  schema_version: 2;
  id: string;
  kind: "project_update" | "internal_digest";
  generated_at: string;
  subject: string;
  preheader: string;
  audience_id: string;
  project_ids: string[];
  sender: string;
  recipients: { to: string[]; cc: string[] };
  summary: string;
  sections: RelaySection[];
  evidence: Array<Record<string, unknown>>;
};

export type TemplateConfig = {
  schema_version: 1;
  name: string;
  accent: string;
  font_family: string;
  footer: string;
};
