# Artifact reference graph

```mermaid
flowchart TD
  action_advance_deal_stage["action<br/><b>advance-deal-stage</b>"]
  action_qualify_lead["action<br/><b>qualify-lead</b>"]
  agent_policy_agent_policy["agent-policy<br/><b>agent-policy</b>"]
  automation_create_demo_activity["automation<br/><b>create-demo-activity</b>"]
  automation_lead_scoring["automation<br/><b>lead-scoring</b>"]
  automation_qualify_from_transcript["automation<br/><b>qualify-from-transcript</b>"]
  binding_pipedrive["binding<br/><b>pipedrive</b>"]
  buying_context_commerce_analytics_buying_context["buying-context<br/><b>commerce-analytics-buying-context</b>"]
  buying_context_data_activation_buying_context["buying-context<br/><b>data-activation-buying-context</b>"]
  commercial_model_company_commercial_model["commercial-model<br/><b>company-commercial-model</b>"]
  company_context_manifest_acme_analytics_company_context["company-context-manifest<br/><b>acme-analytics-company-context</b>"]
  company_profile_company_profile["company-profile<br/><b>company-profile</b>"]
  company_strategy_company_strategy["company-strategy<br/><b>company-strategy</b>"]
  competitor_landscape_company_competitors["competitor-landscape<br/><b>company-competitors</b>"]
  discovery_snapshot_pipedrive_2026_07_01["discovery-snapshot<br/><b>pipedrive-2026-07-01</b>"]
  draft_qualification_followup_email["draft<br/><b>qualification-followup-email</b>"]
  gtm_motion_commerce_analytics_inbound["gtm-motion<br/><b>commerce-analytics-inbound</b>"]
  gtm_motion_commerce_analytics_outbound["gtm-motion<br/><b>commerce-analytics-outbound</b>"]
  gtm_motion_data_activation_product_led["gtm-motion<br/><b>data-activation-product-led</b>"]
  gtm_motion_data_activation_sales_assisted["gtm-motion<br/><b>data-activation-sales-assisted</b>"]
  gtm_motions_commerce_analytics_motions["gtm-motions<br/><b>commerce-analytics-motions</b>"]
  gtm_motions_data_activation_motions["gtm-motions<br/><b>data-activation-motions</b>"]
  icp_commerce_analytics_icp["icp<br/><b>commerce-analytics-icp</b>"]
  icp_data_activation_icp["icp<br/><b>data-activation-icp</b>"]
  identity_identity["identity<br/><b>identity</b>"]
  kpi_new_arr["kpi<br/><b>new-arr</b>"]
  kpi_qualified_to_demo_conversion["kpi<br/><b>qualified-to-demo-conversion</b>"]
  kpi_win_rate["kpi<br/><b>win-rate</b>"]
  loop_lead_qualification["loop<br/><b>lead-qualification</b>"]
  market_overview_company_market_overview["market-overview<br/><b>company-market-overview</b>"]
  messaging_commerce_analytics_messaging["messaging<br/><b>commerce-analytics-messaging</b>"]
  messaging_data_activation_messaging["messaging<br/><b>data-activation-messaging</b>"]
  object_type_deal["object-type<br/><b>deal</b>"]
  object_type_organization["object-type<br/><b>organization</b>"]
  object_type_person["object-type<br/><b>person</b>"]
  operating_model_company_operating_model["operating-model<br/><b>company-operating-model</b>"]
  personas_commerce_analytics_personas["personas<br/><b>commerce-analytics-personas</b>"]
  personas_data_activation_personas["personas<br/><b>data-activation-personas</b>"]
  positioning_commerce_analytics_positioning["positioning<br/><b>commerce-analytics-positioning</b>"]
  positioning_data_activation_positioning["positioning<br/><b>data-activation-positioning</b>"]
  process_new_business["process<br/><b>new-business</b>"]
  product_context_audience_activation["product-context<br/><b>audience-activation</b>"]
  product_context_growth_plan["product-context<br/><b>growth-plan</b>"]
  product_context_scale_plan["product-context<br/><b>scale-plan</b>"]
  product_context_warehouse_sync["product-context<br/><b>warehouse-sync</b>"]
  product_group_manifest_commerce_analytics["product-group<br/><b>commerce-analytics</b>"]
  product_group_manifest_data_activation["product-group<br/><b>data-activation</b>"]
  product_group_strategy_commerce_analytics_strategy["product-group-strategy<br/><b>commerce-analytics-strategy</b>"]
  product_group_strategy_data_activation_strategy["product-group-strategy<br/><b>data-activation-strategy</b>"]
  prompt_lead_qualification["prompt<br/><b>lead-qualification</b>"]
  segment_commerce_analytics_core_segment["segment<br/><b>commerce-analytics-core-segment</b>"]
  segment_data_activation_core_segment["segment<br/><b>data-activation-core-segment</b>"]
  system_pipedrive["system<br/><b>pipedrive</b>"]
  use_case_commerce_analytics_core_use_case["use-case<br/><b>commerce-analytics-core-use-case</b>"]
  use_case_data_activation_core_use_case["use-case<br/><b>data-activation-core-use-case</b>"]
  value_propositions_commerce_analytics_value_propositions["value-propositions<br/><b>commerce-analytics-value-propositions</b>"]
  value_propositions_data_activation_value_propositions["value-propositions<br/><b>data-activation-value-propositions</b>"]
  action_advance_deal_stage --> action_qualify_lead
  action_advance_deal_stage --> automation_create_demo_activity
  action_advance_deal_stage --> object_type_deal
  action_advance_deal_stage --> process_new_business
  action_advance_deal_stage --> system_pipedrive
  action_qualify_lead --> automation_qualify_from_transcript
  action_qualify_lead --> object_type_deal
  action_qualify_lead --> prompt_lead_qualification
  action_qualify_lead --> system_pipedrive
  agent_policy_agent_policy --> action_advance_deal_stage
  agent_policy_agent_policy --> action_qualify_lead
  agent_policy_agent_policy --> object_type_deal
  automation_create_demo_activity --> object_type_deal
  automation_lead_scoring --> object_type_deal
  automation_lead_scoring --> object_type_organization
  automation_lead_scoring --> object_type_person
  automation_qualify_from_transcript --> object_type_deal
  automation_qualify_from_transcript --> prompt_lead_qualification
  binding_pipedrive --> action_qualify_lead
  binding_pipedrive --> automation_lead_scoring
  binding_pipedrive --> automation_qualify_from_transcript
  binding_pipedrive --> object_type_deal
  binding_pipedrive --> object_type_organization
  binding_pipedrive --> object_type_person
  binding_pipedrive --> system_pipedrive
  buying_context_commerce_analytics_buying_context --> icp_commerce_analytics_icp
  buying_context_commerce_analytics_buying_context --> personas_commerce_analytics_personas
  buying_context_commerce_analytics_buying_context --> product_context_growth_plan
  buying_context_commerce_analytics_buying_context --> product_context_scale_plan
  buying_context_commerce_analytics_buying_context --> product_group_manifest_commerce_analytics
  buying_context_commerce_analytics_buying_context --> product_group_strategy_commerce_analytics_strategy
  buying_context_commerce_analytics_buying_context --> segment_commerce_analytics_core_segment
  buying_context_commerce_analytics_buying_context --> use_case_commerce_analytics_core_use_case
  buying_context_data_activation_buying_context --> icp_data_activation_icp
  buying_context_data_activation_buying_context --> personas_data_activation_personas
  buying_context_data_activation_buying_context --> product_context_audience_activation
  buying_context_data_activation_buying_context --> product_context_warehouse_sync
  buying_context_data_activation_buying_context --> product_group_manifest_data_activation
  buying_context_data_activation_buying_context --> product_group_strategy_data_activation_strategy
  buying_context_data_activation_buying_context --> segment_data_activation_core_segment
  buying_context_data_activation_buying_context --> use_case_data_activation_core_use_case
  discovery_snapshot_pipedrive_2026_07_01 --> system_pipedrive
  draft_qualification_followup_email --> process_new_business
  gtm_motions_commerce_analytics_motions --> buying_context_commerce_analytics_buying_context
  gtm_motions_commerce_analytics_motions --> icp_commerce_analytics_icp
  gtm_motions_commerce_analytics_motions --> messaging_commerce_analytics_messaging
  gtm_motions_commerce_analytics_motions --> personas_commerce_analytics_personas
  gtm_motions_commerce_analytics_motions --> positioning_commerce_analytics_positioning
  gtm_motions_commerce_analytics_motions --> product_context_growth_plan
  gtm_motions_commerce_analytics_motions --> product_context_scale_plan
  gtm_motions_commerce_analytics_motions --> product_group_manifest_commerce_analytics
  gtm_motions_commerce_analytics_motions --> product_group_strategy_commerce_analytics_strategy
  gtm_motions_commerce_analytics_motions --> segment_commerce_analytics_core_segment
  gtm_motions_commerce_analytics_motions --> use_case_commerce_analytics_core_use_case
  gtm_motions_commerce_analytics_motions --> value_propositions_commerce_analytics_value_propositions
  gtm_motions_data_activation_motions --> buying_context_data_activation_buying_context
  gtm_motions_data_activation_motions --> icp_data_activation_icp
  gtm_motions_data_activation_motions --> messaging_data_activation_messaging
  gtm_motions_data_activation_motions --> personas_data_activation_personas
  gtm_motions_data_activation_motions --> positioning_data_activation_positioning
  gtm_motions_data_activation_motions --> product_context_audience_activation
  gtm_motions_data_activation_motions --> product_context_warehouse_sync
  gtm_motions_data_activation_motions --> product_group_manifest_data_activation
  gtm_motions_data_activation_motions --> product_group_strategy_data_activation_strategy
  gtm_motions_data_activation_motions --> segment_data_activation_core_segment
  gtm_motions_data_activation_motions --> use_case_data_activation_core_use_case
  gtm_motions_data_activation_motions --> value_propositions_data_activation_value_propositions
  icp_commerce_analytics_icp --> product_group_manifest_commerce_analytics
  icp_commerce_analytics_icp --> product_group_strategy_commerce_analytics_strategy
  icp_commerce_analytics_icp --> segment_commerce_analytics_core_segment
  icp_commerce_analytics_icp --> use_case_commerce_analytics_core_use_case
  icp_data_activation_icp --> product_group_manifest_data_activation
  icp_data_activation_icp --> product_group_strategy_data_activation_strategy
  icp_data_activation_icp --> segment_data_activation_core_segment
  icp_data_activation_icp --> use_case_data_activation_core_use_case
  identity_identity --> object_type_organization
  identity_identity --> object_type_person
  identity_identity --> system_pipedrive
  kpi_new_arr --> object_type_deal
  kpi_new_arr --> process_new_business
  kpi_qualified_to_demo_conversion --> object_type_deal
  kpi_qualified_to_demo_conversion --> process_new_business
  kpi_win_rate --> object_type_deal
  kpi_win_rate --> process_new_business
  loop_lead_qualification --> action_qualify_lead
  loop_lead_qualification --> process_new_business
  loop_lead_qualification --> prompt_lead_qualification
  messaging_commerce_analytics_messaging --> buying_context_commerce_analytics_buying_context
  messaging_commerce_analytics_messaging --> personas_commerce_analytics_personas
  messaging_commerce_analytics_messaging --> positioning_commerce_analytics_positioning
  messaging_commerce_analytics_messaging --> product_context_growth_plan
  messaging_commerce_analytics_messaging --> product_context_scale_plan
  messaging_commerce_analytics_messaging --> product_group_manifest_commerce_analytics
  messaging_commerce_analytics_messaging --> product_group_strategy_commerce_analytics_strategy
  messaging_commerce_analytics_messaging --> segment_commerce_analytics_core_segment
  messaging_commerce_analytics_messaging --> use_case_commerce_analytics_core_use_case
  messaging_commerce_analytics_messaging --> value_propositions_commerce_analytics_value_propositions
  messaging_data_activation_messaging --> buying_context_data_activation_buying_context
  messaging_data_activation_messaging --> personas_data_activation_personas
  messaging_data_activation_messaging --> positioning_data_activation_positioning
  messaging_data_activation_messaging --> product_context_audience_activation
  messaging_data_activation_messaging --> product_context_warehouse_sync
  messaging_data_activation_messaging --> product_group_manifest_data_activation
  messaging_data_activation_messaging --> product_group_strategy_data_activation_strategy
  messaging_data_activation_messaging --> segment_data_activation_core_segment
  messaging_data_activation_messaging --> use_case_data_activation_core_use_case
  messaging_data_activation_messaging --> value_propositions_data_activation_value_propositions
  object_type_deal --> action_advance_deal_stage
  object_type_deal --> action_qualify_lead
  object_type_deal --> automation_lead_scoring
  object_type_deal --> automation_qualify_from_transcript
  object_type_deal --> object_type_organization
  object_type_deal --> object_type_person
  object_type_deal --> process_new_business
  object_type_deal --> prompt_lead_qualification
  object_type_organization --> automation_lead_scoring
  object_type_organization --> object_type_deal
  object_type_person --> automation_lead_scoring
  object_type_person --> loop_lead_qualification
  object_type_person --> object_type_organization
  personas_commerce_analytics_personas --> icp_commerce_analytics_icp
  personas_commerce_analytics_personas --> product_group_manifest_commerce_analytics
  personas_commerce_analytics_personas --> product_group_strategy_commerce_analytics_strategy
  personas_commerce_analytics_personas --> segment_commerce_analytics_core_segment
  personas_commerce_analytics_personas --> use_case_commerce_analytics_core_use_case
  personas_data_activation_personas --> icp_data_activation_icp
  personas_data_activation_personas --> product_group_manifest_data_activation
  personas_data_activation_personas --> product_group_strategy_data_activation_strategy
  personas_data_activation_personas --> segment_data_activation_core_segment
  personas_data_activation_personas --> use_case_data_activation_core_use_case
  positioning_commerce_analytics_positioning --> buying_context_commerce_analytics_buying_context
  positioning_commerce_analytics_positioning --> icp_commerce_analytics_icp
  positioning_commerce_analytics_positioning --> personas_commerce_analytics_personas
  positioning_commerce_analytics_positioning --> product_context_growth_plan
  positioning_commerce_analytics_positioning --> product_context_scale_plan
  positioning_commerce_analytics_positioning --> product_group_manifest_commerce_analytics
  positioning_commerce_analytics_positioning --> product_group_strategy_commerce_analytics_strategy
  positioning_commerce_analytics_positioning --> segment_commerce_analytics_core_segment
  positioning_commerce_analytics_positioning --> use_case_commerce_analytics_core_use_case
  positioning_data_activation_positioning --> buying_context_data_activation_buying_context
  positioning_data_activation_positioning --> icp_data_activation_icp
  positioning_data_activation_positioning --> personas_data_activation_personas
  positioning_data_activation_positioning --> product_context_audience_activation
  positioning_data_activation_positioning --> product_context_warehouse_sync
  positioning_data_activation_positioning --> product_group_manifest_data_activation
  positioning_data_activation_positioning --> product_group_strategy_data_activation_strategy
  positioning_data_activation_positioning --> segment_data_activation_core_segment
  positioning_data_activation_positioning --> use_case_data_activation_core_use_case
  process_new_business --> automation_create_demo_activity
  process_new_business --> draft_qualification_followup_email
  process_new_business --> gtm_motion_commerce_analytics_inbound
  process_new_business --> gtm_motion_commerce_analytics_outbound
  process_new_business --> kpi_qualified_to_demo_conversion
  process_new_business --> kpi_win_rate
  process_new_business --> object_type_deal
  process_new_business --> product_group_manifest_commerce_analytics
  product_context_audience_activation --> buying_context_data_activation_buying_context
  product_context_audience_activation --> gtm_motion_data_activation_sales_assisted
  product_context_audience_activation --> icp_data_activation_icp
  product_context_audience_activation --> personas_data_activation_personas
  product_context_audience_activation --> positioning_data_activation_positioning
  product_context_audience_activation --> product_group_manifest_data_activation
  product_context_audience_activation --> product_group_strategy_data_activation_strategy
  product_context_audience_activation --> segment_data_activation_core_segment
  product_context_audience_activation --> use_case_data_activation_core_use_case
  product_context_growth_plan --> buying_context_commerce_analytics_buying_context
  product_context_growth_plan --> gtm_motion_commerce_analytics_inbound
  product_context_growth_plan --> icp_commerce_analytics_icp
  product_context_growth_plan --> personas_commerce_analytics_personas
  product_context_growth_plan --> positioning_commerce_analytics_positioning
  product_context_growth_plan --> product_group_manifest_commerce_analytics
  product_context_growth_plan --> product_group_strategy_commerce_analytics_strategy
  product_context_growth_plan --> segment_commerce_analytics_core_segment
  product_context_growth_plan --> use_case_commerce_analytics_core_use_case
  product_context_scale_plan --> buying_context_commerce_analytics_buying_context
  product_context_scale_plan --> gtm_motion_commerce_analytics_inbound
  product_context_scale_plan --> gtm_motion_commerce_analytics_outbound
  product_context_scale_plan --> icp_commerce_analytics_icp
  product_context_scale_plan --> personas_commerce_analytics_personas
  product_context_scale_plan --> positioning_commerce_analytics_positioning
  product_context_scale_plan --> product_context_growth_plan
  product_context_scale_plan --> product_group_manifest_commerce_analytics
  product_context_scale_plan --> product_group_strategy_commerce_analytics_strategy
  product_context_scale_plan --> segment_commerce_analytics_core_segment
  product_context_scale_plan --> use_case_commerce_analytics_core_use_case
  product_context_warehouse_sync --> buying_context_data_activation_buying_context
  product_context_warehouse_sync --> gtm_motion_data_activation_product_led
  product_context_warehouse_sync --> gtm_motion_data_activation_sales_assisted
  product_context_warehouse_sync --> icp_data_activation_icp
  product_context_warehouse_sync --> personas_data_activation_personas
  product_context_warehouse_sync --> positioning_data_activation_positioning
  product_context_warehouse_sync --> product_group_manifest_data_activation
  product_context_warehouse_sync --> product_group_strategy_data_activation_strategy
  product_context_warehouse_sync --> segment_data_activation_core_segment
  product_context_warehouse_sync --> use_case_data_activation_core_use_case
  product_group_strategy_commerce_analytics_strategy --> icp_commerce_analytics_icp
  product_group_strategy_commerce_analytics_strategy --> product_group_manifest_commerce_analytics
  product_group_strategy_commerce_analytics_strategy --> segment_commerce_analytics_core_segment
  product_group_strategy_commerce_analytics_strategy --> use_case_commerce_analytics_core_use_case
  product_group_strategy_data_activation_strategy --> icp_data_activation_icp
  product_group_strategy_data_activation_strategy --> product_group_manifest_data_activation
  product_group_strategy_data_activation_strategy --> segment_data_activation_core_segment
  product_group_strategy_data_activation_strategy --> use_case_data_activation_core_use_case
  prompt_lead_qualification --> action_qualify_lead
  prompt_lead_qualification --> object_type_deal
  segment_commerce_analytics_core_segment --> icp_commerce_analytics_icp
  segment_commerce_analytics_core_segment --> personas_commerce_analytics_personas
  segment_commerce_analytics_core_segment --> product_group_manifest_commerce_analytics
  segment_commerce_analytics_core_segment --> product_group_strategy_commerce_analytics_strategy
  segment_commerce_analytics_core_segment --> use_case_commerce_analytics_core_use_case
  segment_data_activation_core_segment --> icp_data_activation_icp
  segment_data_activation_core_segment --> personas_data_activation_personas
  segment_data_activation_core_segment --> product_group_manifest_data_activation
  segment_data_activation_core_segment --> product_group_strategy_data_activation_strategy
  segment_data_activation_core_segment --> use_case_data_activation_core_use_case
  system_pipedrive --> action_advance_deal_stage
  use_case_commerce_analytics_core_use_case --> personas_commerce_analytics_personas
  use_case_commerce_analytics_core_use_case --> product_context_growth_plan
  use_case_commerce_analytics_core_use_case --> product_context_scale_plan
  use_case_commerce_analytics_core_use_case --> product_group_manifest_commerce_analytics
  use_case_commerce_analytics_core_use_case --> product_group_strategy_commerce_analytics_strategy
  use_case_commerce_analytics_core_use_case --> segment_commerce_analytics_core_segment
  use_case_data_activation_core_use_case --> personas_data_activation_personas
  use_case_data_activation_core_use_case --> product_context_audience_activation
  use_case_data_activation_core_use_case --> product_context_warehouse_sync
  use_case_data_activation_core_use_case --> product_group_manifest_data_activation
  use_case_data_activation_core_use_case --> product_group_strategy_data_activation_strategy
  use_case_data_activation_core_use_case --> segment_data_activation_core_segment
  value_propositions_commerce_analytics_value_propositions --> buying_context_commerce_analytics_buying_context
  value_propositions_commerce_analytics_value_propositions --> personas_commerce_analytics_personas
  value_propositions_commerce_analytics_value_propositions --> positioning_commerce_analytics_positioning
  value_propositions_commerce_analytics_value_propositions --> product_context_growth_plan
  value_propositions_commerce_analytics_value_propositions --> product_context_scale_plan
  value_propositions_commerce_analytics_value_propositions --> product_group_manifest_commerce_analytics
  value_propositions_commerce_analytics_value_propositions --> product_group_strategy_commerce_analytics_strategy
  value_propositions_commerce_analytics_value_propositions --> segment_commerce_analytics_core_segment
  value_propositions_commerce_analytics_value_propositions --> use_case_commerce_analytics_core_use_case
  value_propositions_data_activation_value_propositions --> buying_context_data_activation_buying_context
  value_propositions_data_activation_value_propositions --> personas_data_activation_personas
  value_propositions_data_activation_value_propositions --> positioning_data_activation_positioning
  value_propositions_data_activation_value_propositions --> product_context_audience_activation
  value_propositions_data_activation_value_propositions --> product_context_warehouse_sync
  value_propositions_data_activation_value_propositions --> product_group_manifest_data_activation
  value_propositions_data_activation_value_propositions --> product_group_strategy_data_activation_strategy
  value_propositions_data_activation_value_propositions --> segment_data_activation_core_segment
  value_propositions_data_activation_value_propositions --> use_case_data_activation_core_use_case
```

*Generated from ontology `acme-analytics` v1.4.0 (2026-07-15), do not hand-edit.*
