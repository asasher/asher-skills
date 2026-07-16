import { Heading, Hr, Section, Text } from "react-email";
import React from "react";
import { BaseEmail, styles } from "./base.js";
import type { RelayBag, TemplateConfig } from "./types.js";

export function InternalDigestEmail({ bag, config }: { bag: RelayBag; config: TemplateConfig }) {
  return <BaseEmail preheader={bag.preheader} eyebrow="Internal digest" config={config}>
    <Section style={{ padding: "4px 26px 16px" }}>
      <Heading as="h1" className="email-primary" style={styles.heading}>{bag.subject}</Heading>
      <Text className="email-muted" style={styles.summary}>{bag.summary}</Text>
    </Section>
    {bag.sections.map((section, index) => <Section key={section.title} style={{ padding: "0 26px 7px" }}>
      {index ? <Hr className="email-line" style={{ borderColor: "#e5e5e5", margin: "10px 0 14px" }} /> : null}
      {section.subtitle ? <Text className="email-muted" style={styles.status}>{section.subtitle}</Text> : null}
      <Heading as="h2" className="email-primary" style={styles.sectionTitle}>{section.title}</Heading>
      {section.items.length ? section.items.map(item => <Section className="email-item" key={`${item.title}-${item.evidence_ids.join("-")}`} style={{ backgroundColor: "#ffffff", padding: "6px 0 8px" }}>
        <Text className="email-muted" style={styles.status}>{item.visibility ? item.visibility.replace("_", " ") : item.status.replace("_", " ")}</Text>
        <Text className="email-primary" style={styles.itemTitle}>{item.title}</Text>
        <Text className="email-muted" style={styles.itemDetail}>{item.detail}</Text>
      </Section>) : <Text className="email-muted" style={styles.itemDetail}>Nothing verified for this period.</Text>}
    </Section>)}
  </BaseEmail>;
}
