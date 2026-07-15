---
kind: draft
id: qualification-followup-email
meta: {source: declared, status: confirmed, confirmed_by: "Piotr (Head of Sales)", updated: 2026-07-06}
channel: email
used_by:
  - process:new-business/qualified
language: en
variables:
  - {id: first_name, source: person.full_name}
  - {id: company_name, source: organization.name}
  - {id: pain_point, source: "deal.ai_qualification_summary, Need section"}
  - {id: demo_link, source: "AE calendar link"}
approval: required
---

Subject: Next step for {{company_name}}: demo

Hi {{first_name}},

Thanks for the call today. You mentioned {{pain_point}}. The funnel analytics
module is the part of Acme you should see first.

Pick a slot that works for you: {{demo_link}}

Best,
