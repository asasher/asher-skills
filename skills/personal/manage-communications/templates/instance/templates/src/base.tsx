import {
  Body,
  Container,
  Head,
  Hr,
  Html,
  Preview,
  Section,
  Text,
} from "react-email";
import type { ReactNode } from "react";

type BaseEmailProps = {
  preheader: string;
  eyebrow: string;
  children: ReactNode;
};

const orange = "#d95618";
const ink = "#171717";
const muted = "#646464";
const line = "#dedede";

export function BaseEmail({ preheader, eyebrow, children }: BaseEmailProps) {
  return (
    <Html lang="en">
      <Head />
      <Preview>{preheader}</Preview>
      <Body style={{ backgroundColor: "#f4f2ee", margin: 0, padding: "32px 12px" }}>
        <Container
          style={{
            backgroundColor: "#ffffff",
            border: `1px solid ${line}`,
            fontFamily: "Arial, Helvetica, sans-serif",
            margin: "0 auto",
            maxWidth: "640px",
          }}
        >
          <Section style={{ borderTop: `5px solid ${orange}`, padding: "26px 34px 12px" }}>
            <Text
              style={{
                color: orange,
                fontSize: "11px",
                fontWeight: 700,
                letterSpacing: "1.4px",
                margin: 0,
                textTransform: "uppercase",
              }}
            >
              {eyebrow}
            </Text>
          </Section>
          {children}
          <Section style={{ padding: "0 34px 28px" }}>
            <Hr style={{ borderColor: line, margin: "22px 0" }} />
            <Text style={{ color: muted, fontSize: "12px", lineHeight: "18px", margin: 0 }}>
              Prepared with AI, reviewed and sent by Dunn Harland.
            </Text>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}

export const emailStyles = {
  heading: { color: ink, fontSize: "30px", lineHeight: "36px", margin: "0 0 12px" },
  summary: { color: muted, fontSize: "16px", lineHeight: "25px", margin: 0 },
  sectionTitle: { color: ink, fontSize: "18px", lineHeight: "24px", margin: "0 0 12px" },
  itemTitle: { color: ink, fontSize: "14px", fontWeight: 700, lineHeight: "20px", margin: "0 0 4px" },
  itemDetail: { color: muted, fontSize: "14px", lineHeight: "22px", margin: 0 },
  status: { color: orange, fontSize: "10px", fontWeight: 700, letterSpacing: "1px", margin: "0 0 6px", textTransform: "uppercase" as const },
};
