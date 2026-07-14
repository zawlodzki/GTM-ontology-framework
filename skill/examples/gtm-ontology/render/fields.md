# Field dictionary

## Deal

A concrete revenue opportunity with an identified organization: someone at the account has shown buying intent worth SDR/AE time. Not every form-fill becomes a deal; see process:new-business Incoming entry criteria.

| Field | Type | Required | Filled by | Values |
|---|---|---|---|---|
| **Title** | string |  | mixed |  |
| **Pipeline Stage** | enum |  | mixed | **incoming**: see process:new-business/incoming<br>**qualified**: see process:new-business/qualified<br>**demo**: see process:new-business/demo<br>**proposal**: see process:new-business/proposal<br>**negotiation**: see process:new-business/negotiation<br>**won**: see process:new-business/won<br>**lost**: see process:new-business/lost |
| **Amount** | currency | from stage qualified | human |  |
| **Expected Close Date** | date | from stage qualified | human |  |
| **Source Channel** | enum |  | mixed | **inbound-form**: Website demo-request or content form submission<br>**outbound**: Sourced by SDR sequence (email/LinkedIn)<br>**referral**: Introduced by existing customer or partner |
| **Budget Confirmed** | boolean |  | human |  |
| **AI Qualification Summary** | text |  | ai |  |
| **AI Qualification Score** | number |  | ai |  |

## Organization

A company we sell to, prospect account or customer.

| Field | Type | Required | Filled by | Values |
|---|---|---|---|---|
| **Name** | string |  | mixed |  |
| **Domain** | string |  | mixed |  |
| **Industry** | string |  | integration |  |
| **Employee Count** | number |  | integration |  |
| **ICP Fit** | boolean |  | automation |  |

## Person

An individual we market or sell to, i.e. lead, contact, or user at a customer.

| Field | Type | Required | Filled by | Values |
|---|---|---|---|---|
| **Email** | string |  | mixed |  |
| **Full Name** | string |  | mixed |  |
| **Job Title** | string |  | mixed |  |
| **Engagement Score** | number |  | automation |  |
| **Lifecycle Stage** | enum |  | mixed | **Lead**: Known email, no ICP/engagement threshold crossed yet.<br>**MQL**: Organization matches ICP (org.icp_fit == true) AND engagement_score >= 40 within the last 30 days.<br><br>**SQL**: SDR spoke with the person, confirmed fit and interest, and a deal was created or is being created. Human judgment call; no automation sets this.<br><br>**Opportunity**: Primary contact on a deal that reached Qualified or beyond.<br>**Customer**: Contact at an organization with at least one won deal. |

*Generated from ontology `acme-analytics` v1.3.0 (2026-07-14), do not hand-edit.*
