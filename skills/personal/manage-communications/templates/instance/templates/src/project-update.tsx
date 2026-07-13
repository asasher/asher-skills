import { Heading, Hr, Section, Text } from "react-email";
import { BaseEmail, emailStyles } from "./base.js";
import type { CommsBag } from "./types.js";

export function ProjectUpdateEmail({ bag }: { bag: CommsBag }) {
  return (
    <BaseEmail preheader={bag.preheader} eyebrow="Project update">
      <Section style={{ padding: "8px 34px 24px" }}>
        <Heading as="h1" style={emailStyles.heading}>{bag.subject}</Heading>
        <Text style={emailStyles.summary}>{bag.summary}</Text>
      </Section>
      {bag.sections.map((section, sectionIndex) => (
        <Section key={section.title} style={{ padding: "0 34px 8px" }}>
          {sectionIndex > 0 ? <Hr style={{ borderColor: "#dedede", margin: "14px 0 22px" }} /> : null}
          <Heading as="h2" style={emailStyles.sectionTitle}>{section.title}</Heading>
          {section.items.length === 0 ? (
            <Text style={emailStyles.itemDetail}>Nothing verified for this period.</Text>
          ) : section.items.map((item) => (
            <Section key={`${item.title}-${item.evidence_ids.join("-")}`} style={{ padding: "0 0 18px" }}>
              <Text style={emailStyles.status}>{item.status.replaceAll("_", " ")}</Text>
              <Text style={emailStyles.itemTitle}>{item.title}</Text>
              <Text style={emailStyles.itemDetail}>{item.detail}</Text>
            </Section>
          ))}
        </Section>
      ))}
    </BaseEmail>
  );
}
