# STADIOEquities — Customer Activation and Engagement: Data Extract

Clients registered between September 2022 and August 2026. Nine CSV tables joined on `client_id`; `account_id` additionally links the account-level tables. Both are anonymised and non-reversible — no PII is included. Datetimes are `yyyy-MM-dd HH:mm:ss` in SAST; amounts are ZAR. Extract date is 31 August 2026.

## Files

### `table1_client_account.csv`
One row per client: the base population, with account state, demographics and acquisition.  
Rows: 3,109

| Column | Description |
|---|---|
| `client_id` | Unique anonymised client identifier. Consistent across all nine tables. |
| `account_id` | Unique investment account identifier. |
| `registration_date` | Date and time the account was created. |
| `account_status` | Registered, Active, Dormant or Closed. |
| `activation_date` | Date the client first met the activation definition. Empty if never activated. |
| `first_deposit_date` | Date and time of first successful deposit. Empty for never-funded clients. |
| `account_closure_date` | Empty if the account remains open. |
| `kyc_status` | Not Started, In Progress, Complete, Failed. |
| `kyc_completion_date` | Empty if KYC was not completed. |
| `age` | Age in completed years at registration. |
| `province_region` | Province recorded at registration. |
| `stated_investment_goal` | Goal category captured at sign-up. |
| `risk_appetite` | Low, Moderate, High. |
| `client_segment` | Existing internal segment: Retail, Mass affluent, Professional. Not created for this extract. |
| `acquisition_channel` | Channel the client was acquired through. |
| `acquisition_campaign` | Campaign identifier. Empty where the sign-up is not campaign-attributed. |
| `acquisition_cost` | Cost attributed to acquiring the account, ZAR. |
| `latest_activity_date` | Most recent qualifying account activity. |
| `days_since_last_activity` | Days from `latest_activity_date` to the extract date (31 August 2026). |
| `funded_flag` | TRUE if the account has ever received a successful deposit. |
| `active_flag` | TRUE where the account is currently active — traded or held in the last 90 days. |
| `dormant_flag` | Current internal dormancy classification. See the definitions note below. |

### `table2_onboarding_kyc_journey.csv`
One row per onboarding/KYC step event. A client has rows up to the furthest step they reached.  
Rows: 20,169

| Column | Description |
|---|---|
| `client_id` | Links to the client table. |
| `account_id` | Links to the account table. |
| `onboarding_session_id` | Unique onboarding session identifier. |
| `step_name` | Account Created, Identity Verification, Address Verification, Bank Link, Risk Questionnaire, Selfie Check, Onboarding Complete. |
| `step_number` | Sequential position within the onboarding journey (1–7). |
| `step_start_time` | When the client entered the step. |
| `step_completion_time` | Empty where the step was abandoned. |
| `step_completed` | TRUE if completed successfully. |
| `abandoned_flag` | TRUE where the client left before completion. |
| `abandonment_reason` | Recorded reason. Empty where the step completed. |
| `error_code` | System error encountered during onboarding. Empty where none occurred. |
| `retry_count` | Attempts at this step. |
| `time_on_step` | Seconds spent on the step. |
| `device_type` | Mobile, Desktop, Tablet. |
| `platform` | Android, iOS, Web. |
| `app_version` | Client app version, useful for spotting release-related friction. |
| `referral_source` | Source immediately before onboarding, where captured. |

### `table3_app_web_behaviour.csv`
One row per app/web event, as requested — raw events rather than summary statistics only. Session-level fields are carried on each event row of that session.  
Rows: 71,052

| Column | Description |
|---|---|
| `client_id` | Anonymised client identifier. |
| `session_id` | Unique browsing/app session. |
| `event_id` | Unique event identifier. |
| `event_datetime` | Exact event timestamp. |
| `event_type` | Screen View, Button Click, Search, Login, Logout, Error. |
| `screen_name` | Screen viewed. |
| `feature_name` | Feature being used. |
| `action` | View, Click, Submit, Scroll. |
| `session_start` | Start of the session the event belongs to. Repeated on every event row in that session. |
| `session_end` | End of the session. Repeated on every event row. |
| `session_duration` | Session length in seconds. Session-level, repeated on each event row. |
| `screens_viewed` | Events in the session. Session-level, repeated on each event row. |
| `device_type` | Device category. |
| `operating_system` | Android, iOS, Windows, macOS. |
| `app_web` | App or Web. |
| `login_status` | Authenticated or Guest. |
| `error_encountered` | TRUE where a technical error occurred. |
| `error_code` | Empty where no error occurred. |
| `search_term` | Populated only for Search events. |
| `days_since_registration` | Days from registration to the event. |
| `days_since_previous_session` | Days since the client's previous session. Empty for a first session. |

### `table4_funding_transactions.csv`
One row per financial movement. Funded clients only.  
Rows: 5,448

| Column | Description |
|---|---|
| `client_id` | Links to the client table. |
| `account_id` | Account involved. |
| `transaction_id` | Unique transaction identifier. |
| `transaction_datetime` | When the transaction occurred. |
| `transaction_type` | Deposit, Withdrawal, Transfer. |
| `transaction_status` | Successful, Pending, Failed, Reversed. |
| `amount` | Transaction amount, ZAR. |
| `balance_before` | Cash balance before the transaction. |
| `balance_after` | Cash balance after the transaction. |
| `deposit_method` | EFT, Instant EFT, Debit Card, Debit Order, Cash Deposit. Empty for non-deposits. |
| `deposit_sequence` | 1 for the first successful deposit, 2 for the second, and so on. Empty for non-deposits and failures. |
| `failure_reason` | Populated for failed deposits. |
| `days_since_registration` | Days between account creation and this funding event. |
| `first_deposit_flag` | TRUE on the first successful deposit. |

### `table5_trading_portfolio.csv`
One row per trade. Funded clients only.  
Rows: 10,503

| Column | Description |
|---|---|
| `client_id` | Client identifier. |
| `account_id` | Investment account. |
| `trade_id` | Unique trade identifier. |
| `trade_datetime` | Exact trade timestamp. |
| `trade_type` | Buy or Sell. |
| `instrument_id` | Instrument identifier/ticker. |
| `instrument_type` | Share, ETF, Bundle, Offshore asset. |
| `quantity` | Units traded; fractional shares preserved. |
| `trade_value` | Total ZAR value of the transaction. |
| `fees` | Total fees charged, ZAR. |
| `portfolio_value` | Portfolio value at the trade date. |
| `cash_balance` | Uninvested cash balance. |
| `number_holdings` | Instruments held at that point. |
| `largest_holding_pct` | Percentage of the portfolio in the largest position. |
| `days_since_previous_trade` | Empty for a client's first trade. |
| `trade_sequence` | The client's nth trade. |

### `table6_marketing_communications.csv`
One row per marketing or onboarding communication event.  
Rows: 12,757

| Column | Description |
|---|---|
| `client_id` | Links across data sources. |
| `communication_id` | Unique communication identifier. |
| `campaign_id` | Marketing or onboarding campaign. |
| `communication_type` | Email, SMS, Push, In-app. |
| `message_category` | Business purpose of the communication. |
| `sent_datetime` | When it was sent. |
| `delivered` | Delivery status. |
| `opened` | Whether it was opened or viewed. |
| `open_datetime` | Empty if not opened. |
| `clicked` | Whether the client clicked through. |
| `click_datetime` | Empty if no click. |
| `converted` | Whether the intended action followed. |
| `conversion_datetime` | Time of conversion. Empty where there was none. |
| `days_after_registration` | Communication timing relative to sign-up. |
| `opt_out_flag` | TRUE where the client has opted out of that channel. |

### `table7_product_subscription.csv`
One row per product or subscription event. Funded clients only.  
Rows: 2,283

| Column | Description |
|---|---|
| `client_id` | Client identifier. |
| `account_id` | Investment account. |
| `product_id` | Product identifier. |
| `product_type` | Tax-Free Account, Standard Account, Retirement Annuity, Offshore Account. |
| `subscription_tier` | Standard, Premium, Premium Plus. |
| `start_date` | Date the product or subscription started. |
| `cancellation_date` | Empty if still active. |
| `subscription_status` | Active, Cancelled, Expired, Trial. |
| `monthly_fee` | Fee in ZAR; 0.00 on the Standard tier. |
| `cancellation_reason` | Captured reason. Empty where not cancelled. |
| `product_usage_count` | Interactions with the product over the extract window. |

### `table8_support_interactions.csv`
One row per support ticket or interaction.  
Rows: 2,256

| Column | Description |
|---|---|
| `client_id` | Client identifier. |
| `ticket_id` | Unique support interaction. |
| `created_datetime` | Ticket creation time. |
| `closed_datetime` | Empty where unresolved. |
| `contact_channel` | Email, Chat, Phone, Web. |
| `ticket_category` | Existing classification. |
| `ticket_subcategory` | More detailed categorisation. |
| `query_text` | De-identified free text of the client's query. |
| `resolution_status` | Resolved, Open, Escalated. |
| `resolution_time` | Minutes to resolution. Empty where unresolved. |
| `escalated` | TRUE where the ticket required escalation. |
| `repeat_contact_flag` | TRUE where the client contacted support repeatedly about the same issue. |
| `satisfaction_score` | 1–5 scale. Empty where no survey response was received. |
| `complaint_flag` | TRUE where the interaction became a formal complaint. |

### `table9_outcome_target.csv`
One row per client: the historical labels for both models.  
Rows: 3,109

| Column | Description |
|---|---|
| `client_id` | Links the outcome to predictor data. |
| `registration_date` | Required for defining the activation observation window. |
| `ever_funded` | TRUE if the client has ever successfully deposited. |
| `first_deposit_date` | Empty for never-funded accounts. |
| `activation_outcome` | **Activation target.** TRUE where the client activated. See the definition note below. |
| `days_to_activation` | Days from registration to activation. Empty where never activated. |
| `dormancy_date` | Date the client met the dormancy definition. Empty where never dormant. |
| `dormancy_outcome` | **Dormancy target.** TRUE where the client became dormant. |
| `reactivation_date` | Empty where the client did not reactivate. |
| `reactivated_flag` | TRUE if the client later became active again. |
| `account_closed` | TRUE where the account was closed. Kept separate from dormancy. |

## Data quality notes

This is an extract from live operational systems and has **not** been cleaned. Expect:

- Missing values in optional / conditionally-populated fields
- Inconsistent casing and stray whitespace in some categorical fields
- A small number of duplicate records
- Occasional out-of-range or implausible values from data-capture errors
- Some date fields captured in inconsistent formats

## Definitions applied in this extract

The request asked for these to be confirmed before modelling. This is what the extract actually uses — if your project needs a different definition, rebuild the label from the raw tables rather than editing table 9.

**Activation.** A client is activated on their **first successful deposit**, not on first deposit plus a trade. `activation_date` in table 1 and `activation_outcome` in table 9 both follow that rule. A small number of clients deposited but never fully activated in the source system, so `ever_funded` and `activation_outcome` are not identical — do not treat them as the same column.

**Dormancy.** A funded account with **90 or more consecutive days** without a trade or deposit, measured inside its first six months. Reactivation is tracked separately: `dormancy_outcome` stays TRUE for a client who later returned, with `reactivated_flag` marking the return. Account closure is a separate field again, so permanent disengagement and dormancy can be distinguished.

## Targets and leakage

**Two targets, two different feature sets.**

- *Activation*: predict `activation_outcome` (table 9) using only information available at or shortly after registration — tables 1 (registration-time fields), 2, 3 and 6, filtered to events before the deposit.
- *Dormancy*: predict `dormancy_outcome` (table 9) for funded clients only, using behaviour in the period after funding.

**Leakage warning.** Table 9 is outcome data throughout and must never be used as a feature. In table 1, `account_status`, `activation_date`, `first_deposit_date`, `account_closure_date`, `latest_activity_date`, `days_since_last_activity`, `funded_flag`, `active_flag` and `dormant_flag` are all current-state or post-outcome fields — for the activation model, only the registration-time fields in table 1 are safe. Tables 4, 5 and 7 exist only for clients who funded, so their mere presence encodes the activation outcome; they are legitimate inputs for the dormancy model but not for the activation model. In tables 3 and 6, filter to events dated before the prediction point.

**Trends present in the data.** KYC abandonment rises from roughly 13% to 18% across the window, sign-up to first-deposit conversion falls from roughly 64% to 59%, and six-month dormancy rises from roughly 22% to 31% — consistent with the briefing pack.

**Coverage.** App/web behaviour is capped at a sample of sessions per client to keep the extract to a workable size, so session counts here are lower than the true platform totals. Support data covers the last three years only, as the briefing states.

_Synthetic data supplied for the CAP182 capstone project. Not real client data._
