---
kind: draft
id: qualification-followup-email
meta: {source: declared, status: draft, updated: 2026-01-01}
channel: email                    # email | sms | linkedin | other
used_by:
  - process:new-business/qualified    # stages referencing this draft
language: pl
variables:                        # placeholders the sender/agent must fill
  - {id: first_name, source: person.full_name}
  - {id: pain_point, source: "deal.ai_qualification_summary, Need section"}
approval: required                # agents never send drafts autonomously unless policy says otherwise
---

<!-- The template body. Placeholders in {{...}}. -->

Temat: Podsumowanie rozmowy – {{company_name}}

Cześć {{first_name}},

dzięki za rozmowę. Tak jak ustaliliśmy...

{{pain_point}}

Pozdrawiam,
