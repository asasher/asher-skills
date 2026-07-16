import { Body, Container, Head, Hr, Html, Preview, Section, Text } from "react-email";
import React, { type ReactNode } from "react";
import type { TemplateConfig } from "./types.js";

type Props = { preheader: string; eyebrow: string; config: TemplateConfig; children: ReactNode };
const ink = "#171717";
const muted = "#737373";
const line = "#e5e5e5";

export function BaseEmail({ preheader, eyebrow, config, children }: Props) {
  return (
    <Html lang="en">
      <Head>
        <meta content="light dark" name="color-scheme" />
        <meta content="light dark" name="supported-color-schemes" />
        <style>{`
          :root { color-scheme: light dark; supported-color-schemes: light dark; }
          @media (prefers-color-scheme: dark) {
            .email-body,.email-canvas,.email-container,.email-item { background-color:#171717!important; }
            .email-primary { color:#e5e5e5!important; } .email-muted { color:#a3a3a3!important; }
            .email-line { border-color:#333333!important; }
          }
          html.dark-preview .email-body,html.dark-preview .email-canvas,html.dark-preview .email-container,
          html.dark-preview .email-item { background-color:#171717!important; }
          html.dark-preview .email-primary { color:#e5e5e5!important; }
          html.dark-preview .email-muted { color:#a3a3a3!important; }
          html.dark-preview .email-line { border-color:#333333!important; }
          html.light-preview .email-body,html.light-preview .email-canvas { background-color:#f5f5f5!important; }
          html.light-preview .email-container,html.light-preview .email-item { background-color:#ffffff!important; }
          html.light-preview .email-primary { color:#171717!important; }
          html.light-preview .email-muted { color:#737373!important; }
          html.light-preview .email-line { border-color:#e5e5e5!important; }
        `}</style>
      </Head>
      <Preview>{preheader}</Preview>
      <Body className="email-body" style={{ backgroundColor: "#f5f5f5", margin: 0 }}>
        <Section className="email-canvas" style={{ backgroundColor: "#f5f5f5", padding: "20px 10px" }}>
          <Container className="email-container" style={{ backgroundColor: "#ffffff", fontFamily: config.font_family, margin: "0 auto", maxWidth: "640px" }}>
            <Section style={{ borderTop: `4px solid ${config.accent}`, padding: "16px 26px 8px" }}>
              {config.name ? <Text className="email-primary" style={{ color: ink, fontSize: "15px", fontWeight: 700, margin: "0 0 4px" }}>{config.name}</Text> : null}
              <Text style={{ color: config.accent, fontSize: "10px", fontWeight: 700, letterSpacing: "1.2px", margin: 0, textTransform: "uppercase" }}>{eyebrow}</Text>
            </Section>
            {children}
            <Section style={{ padding: "0 26px 20px" }}>
              <Hr className="email-line" style={{ borderColor: line, margin: "14px 0" }} />
              <Text className="email-muted" style={{ color: muted, fontSize: "11px", lineHeight: "16px", margin: 0 }}>{config.footer}</Text>
            </Section>
          </Container>
        </Section>
      </Body>
    </Html>
  );
}

export const styles = {
  heading: { color: ink, fontSize: "24px", lineHeight: "30px", margin: "0 0 8px" },
  summary: { color: muted, fontSize: "14px", lineHeight: "21px", margin: 0 },
  sectionTitle: { color: ink, fontSize: "16px", lineHeight: "21px", margin: "0 0 9px" },
  itemTitle: { color: ink, fontSize: "13px", fontWeight: 700, lineHeight: "18px", margin: "0 0 2px" },
  itemDetail: { color: muted, fontSize: "13px", lineHeight: "18px", margin: 0 },
  status: { color: muted, fontSize: "9px", fontWeight: 700, letterSpacing: "0.9px", margin: "0 0 2px", textTransform: "uppercase" as const },
};
