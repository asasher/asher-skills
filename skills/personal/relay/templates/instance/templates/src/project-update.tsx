import { Heading, Hr, Section, Text } from "react-email";
import React from "react";
import { BaseEmail, styles } from "./base.js";
import type { RelayBag, TemplateConfig } from "./types.js";

const labels: Record<string, string> = { production_verified: "Verified", shipped_unverified: "Ready for verification", in_progress: "In progress", pending: "Pending", planned: "Planned" };

export function ProjectUpdateEmail({ bag, config }: { bag: RelayBag; config: TemplateConfig }) {
  return <BaseEmail preheader={bag.preheader} eyebrow="Project update" config={config}>
    <Section style={{ padding: "4px 26px 16px" }}>
      <Heading as="h1" className="email-primary" style={styles.heading}>{bag.subject}</Heading>
      <Text className="email-muted" style={styles.summary}>{bag.summary}</Text>
    </Section>
    {bag.sections.map((section, index) => <Section key={section.title} style={{ padding: "0 26px 4px" }}>
      {index ? <Hr className="email-line" style={{ borderColor: "#e5e5e5", margin: "8px 0 14px" }} /> : null}
      <Heading as="h2" className="email-primary" style={styles.sectionTitle}>{section.title}</Heading>
      {section.items.length ? section.items.map(item => <Section className="email-item" key={`${item.title}-${item.evidence_ids.join("-")}`} style={{ backgroundColor: "#ffffff", padding: "6px 0 8px" }}>
        <Text className="email-muted" style={styles.status}>{labels[item.status] ?? item.status}</Text>
        <Text className="email-primary" style={styles.itemTitle}>{item.title}</Text>
        <Text className="email-muted" style={styles.itemDetail}>{item.detail}</Text>
      </Section>) : <Text className="email-muted" style={styles.itemDetail}>Nothing verified for this period.</Text>}
    </Section>)}
  </BaseEmail>;
}
